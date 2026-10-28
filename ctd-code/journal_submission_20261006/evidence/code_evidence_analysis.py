"""Read-only, standard-library audit of supplied artifacts; never loads models."""
import ast
import collections
import csv
import hashlib
import io
import json
import pathlib
import pickle
import statistics
import zipfile

SOURCE = pathlib.Path('/mnt/user-ssd/zengboyi/ctd/ctd_ppt_data/ctd_ppt_data/CTD')
OUTPUT = pathlib.Path(__file__).with_name('code_results_summary.json')


def identity(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            digest.update(block)
    return {'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest.hexdigest()}


def quantile(values, q):
    values = sorted(values)
    position = (len(values) - 1) * q
    lo = int(position)
    hi = min(lo + 1, len(values) - 1)
    return values[lo] + (values[hi] - values[lo]) * (position - lo)


summary = {'audit_type': 'static code inspection and direct descriptive artifact counts; no model execution',
           'source_directory': str(SOURCE), 'model_metrics_reproduced': False}
wrong = SOURCE / 'CTD/graphsage_wrong_predictions_all.csv'
top = SOURCE / 'CTD/graphsage_top10_wrong_predictions.csv'
with wrong.open(encoding='utf-8-sig', newline='') as stream:
    reader = csv.DictReader(stream)
    header = reader.fieldnames
    rows = list(reader)
with top.open(encoding='utf-8-sig', newline='') as stream:
    top_rows = list(csv.DictReader(stream))
scores = [float(row['预测概率']) for row in rows]
pair_counts = collections.Counter((row['化合物名'], row['疾病名']) for row in rows)
summary['wrong_predictions'] = {
    **identity(wrong), 'columns': header, 'rows': len(rows),
    'unique_compound_names': len({row['化合物名'] for row in rows}),
    'unique_disease_names': len({row['疾病名'] for row in rows}),
    'unique_name_pairs': len(pair_counts),
    'duplicate_name_pair_rows_beyond_first': len(rows) - len(pair_counts),
    'name_pairs_with_multiple_rows': sum(count > 1 for count in pair_counts.values()),
    'exact_duplicate_rows_beyond_first': len(rows) - len({tuple(row.items()) for row in rows}),
    'rows_with_missing_field_values': sum(any(not value for value in row.values()) for row in rows),
    'scores': {'min': min(scores), 'max': max(scores), 'mean': statistics.mean(scores),
               'quantiles_linear': {str(q): quantile(scores, q) for q in [0.25, 0.5, 0.75, 0.9, 0.95, 0.99]},
               'counts_ge': {str(q): sum(value >= q for value in scores) for q in [0.5, 0.9, 0.95, 0.99, 0.999]}},
    'sorted_descending': all(a >= b for a, b in zip(scores, scores[1:])),
    'top10_matches_first10': top_rows == rows[:10],
    'top10_name_pairs_found_anywhere_in_all_file': sum((row['化合物名'], row['疾病名']) in pair_counts for row in top_rows),
    'top10': top_rows,
    'interpretation': 'Selected misclassified records. Probability is maximum predicted-class softmax, not necessarily association probability. True/predicted labels, stable IDs, full test set, and run identity are absent; classification metrics cannot be reconstructed.'
}
first1000 = rows[:1000]
summary['wrong_predictions']['first1000'] = {
    'rows': len(first1000),
    'unique_compound_names': len({row['化合物名'] for row in first1000}),
    'unique_disease_names': len({row['疾病名'] for row in first1000}),
    'unique_name_pairs': len({(row['化合物名'], row['疾病名']) for row in first1000}),
    'top_compound_name_counts': collections.Counter(row['化合物名'] for row in first1000).most_common(20),
    'top_disease_name_counts': collections.Counter(row['疾病名'] for row in first1000).most_common(20),
    'score_min': min(float(row['预测概率']) for row in first1000),
    'score_max': max(float(row['预测概率']) for row in first1000),
    'interpretation': 'First 1000 confidence-ranked errors; selection includes both possible error directions because labels were not exported.'
}


def tensor_metadata(storage, offset, size, stride, requires_grad, hooks, *args):
    return {'shape': list(size), 'stride': list(stride), 'storage_offset': offset, 'storage': storage}


class TensorMetadataReader(pickle.Unpickler):
    """Whitelist-only metadata reader: never imports torch or invokes file globals."""
    def find_class(self, module, name):
        if (module, name) == ('collections', 'OrderedDict'):
            return collections.OrderedDict
        if (module, name) == ('torch._utils', '_rebuild_tensor_v2'):
            return tensor_metadata
        if module == 'torch' and name in ('FloatStorage', 'LongStorage'):
            return name
        raise pickle.UnpicklingError(f'Disallowed global: {module}.{name}')

    def persistent_load(self, pid):
        return list(pid)


summary['checkpoint_metadata'] = {}
for path in sorted((SOURCE / 'CTD').glob('*.pt')):
    with zipfile.ZipFile(path) as archive:
        member = next(name for name in archive.namelist() if name.endswith('/data.pkl'))
        metadata = TensorMetadataReader(io.BytesIO(archive.read(member))).load()
    summary['checkpoint_metadata'][path.name] = {
        'bytes': path.stat().st_size,
        'tensor_shapes': {key: value['shape'] for key, value in metadata.items()},
        'interpretation': 'Tensor metadata only, no tensor storage loaded and no model executed. No dataset or run identity is supplied.'
    }
summary['sider_format_tsvs'] = {}
for name in ['meddra_all_se.tsv', 'meddra_freq.tsv']:
    path = SOURCE / name
    widths = collections.Counter()
    term_types = collections.Counter()
    drugs = set()
    stereo = set()
    concepts = set()
    names = set()
    pt_drugs = set()
    pt_concepts = set()
    pt_names = set()
    pt_pairs = set()
    total_lines = 0
    blank_lines = 0
    for line in path.open(encoding='utf-8'):
        total_lines += 1
        if not line.strip():
            blank_lines += 1
            continue
        fields = line.rstrip('\r\n').split('\t')
        widths[len(fields)] += 1
        expected = 6 if name == 'meddra_all_se.tsv' else 10
        if len(fields) != expected:
            continue
        term_position = 3 if expected == 6 else 7
        concept_position = 4 if expected == 6 else 8
        term_type = fields[term_position]
        concept = fields[concept_position]
        term_name = fields[-1]
        term_types[term_type] += 1
        drugs.add(fields[0])
        stereo.add(fields[1])
        concepts.add(concept)
        names.add(term_name)
        if term_type == 'PT':
            pt_drugs.add(fields[0])
            pt_concepts.add(concept)
            pt_names.add(term_name)
            pt_pairs.add((fields[0], concept))
    summary['sider_format_tsvs'][name] = {
        **identity(path), 'physical_lines': total_lines, 'blank_lines': blank_lines,
        'nonblank_rows_by_field_count': dict(widths), 'term_type_rows': dict(term_types),
        'unique_flat_drug_ids_all_rows': len(drugs), 'unique_stereo_drug_ids_all_rows': len(stereo),
        'unique_mapped_concepts_all_rows': len(concepts), 'unique_mapped_names_all_rows': len(names),
        'pt_unique_flat_drug_ids': len(pt_drugs), 'pt_unique_mapped_concepts': len(pt_concepts),
        'pt_unique_mapped_names': len(pt_names), 'pt_unique_drug_concept_pairs': len(pt_pairs),
        'interpretation': 'SIDER-format adverse-event rows. Counts are artifact descriptions, not CTD graph dimensions or evidence that the supplied models trained on SIDER.'
    }
summary['source_checks'] = {}
for path in sorted(SOURCE.glob('*.py')):
    check = {'syntax': 'ok', 'main_constants': {}, 'loader_assignment_arity': []}
    try:
        tree = ast.parse(path.read_text(encoding='utf-8'))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'main':
                for stmt in node.body:
                    if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
                        key = stmt.targets[0].id
                        if key.isupper():
                            try:
                                check['main_constants'][key] = {'value': ast.literal_eval(stmt.value), 'line': stmt.lineno}
                            except (ValueError, TypeError):
                                pass
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == 'load_and_preprocess_data':
                target = node.targets[0]
                check['loader_assignment_arity'].append({'line': node.lineno, 'arity': len(target.elts) if isinstance(target, ast.Tuple) else None})
    except SyntaxError as error:
        check = {'syntax': type(error).__name__, 'line': error.lineno, 'message': error.msg}
    summary['source_checks'][path.name] = check
summary['logs'] = {}
for path in sorted(SOURCE.glob('*.log')):
    lines = path.read_text(encoding='utf-8').splitlines()
    summary['logs'][path.name] = {**identity(path), 'lines': len(lines), 'terminal_line': lines[-1] if lines else None, 'contains_numeric_training_metrics': False}
summary['referenced_inputs'] = []
for name in ['CTD_chemicals_diseases.csv', 'direct_evidence_relationships.csv', 'high_inference_score_relationships.csv', '环境污染物_pubchemCID.json']:
    path = pathlib.Path('/home/byzeng/hjwrw_all_data') / name
    summary['referenced_inputs'].append({'path': str(path), 'exists': path.exists(), 'present_in_audited_CTD_directory': bool(list(SOURCE.rglob(name)))})
OUTPUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({key: value for key, value in summary.items() if key in ['wrong_predictions', 'sider_format_tsvs']}, ensure_ascii=False, indent=2))
