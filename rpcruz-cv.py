import argparse
parser = argparse.ArgumentParser()
parser.add_argument('type', choices=['html', 'latex'])
args = parser.parse_args()

from tqdm import tqdm
from datetime import datetime
import papers, out

out = getattr(out, args.type.title())()

#################################### START ####################################

out.begin('Ricardo Cruz, PhD')
out.contacts([
    ('profile-email', 'rpcruz@fe.up.pt', 'mailto:rpcruz@fe.up.pt'),
    ('profile-orcid', '0000-0002-5189-6228', 'https://orcid.org/0000-0002-5189-6228'),
    ('profile-github', 'github.com/rpmcruz', 'https://github.com/rpmcruz?tab=repositories'),
])
out.paragraph('Ricardo Cruz has worked on a wide range of machine learning topics, with particular emphasis on deep learning and computer vision. Since 2021, he is a researcher on autonomous driving under the THEIA research project, a partnership between the University of Porto and Bosch Car Multimedia. Prior to that, he was a researcher at INESC TEC since 2015, working towards his PhD in Computer Science. He has a BSc in computer science and a MSc in applied mathematics.')

#################################### PAPERS ####################################

table = [
    ('10.1007/978-3-031-49018-7_40', 'applications'),
    ('10.1007/978-3-031-49018-7_39', 'others'),
    ('10.1007/978-3-031-49018-7_38', 'human-in-the-loop'),
    ('10.1007/978-3-031-36616-1_22', 'human-in-the-loop'),
    ('10.1007/978-3-031-43078-7_43', 'ordinal-losses'),
    ('10.3390/s23063092', 'spatial-resource-efficiency'),
    ('10.1117/12.2679881', 'spatial-resource-efficiency'),
    ('10.1016/j.iswa.2022.200170', 'applications'),
    ('10.3390/math10060980', 'ordinal-losses'),
    ('10.7717/peerj-cs.457', 'ordinal-losses'),
    ('10.1109/ICPR48806.2021.9413004', 'background-invariance'),
    ('10.1109/EMBC.2019.8857385', 'absolute-costs'),
    ('10.1016/j.compeleceng.2019.08.001', 'applications'),
    ('10.1007/978-3-030-30484-3_10', 'others'),
    ('10.1109/IJCNN.2018.8489696', 'iterative-inference'),
    ('10.1109/PRNI.2018.8423960', 'ranking-for-class-imbalance'),
    ('10.1007/s10044-018-0705-4', 'ranking-for-class-imbalance'),
    ('10.1007/978-3-319-59147-6_47', 'absolute-costs'),
    ('10.1007/978-3-319-59147-6_45', 'ranking-for-class-imbalance'),
    ('10.1007/978-3-319-59147-6_46', 'ranking-for-class-imbalance'),
    ('10.1007/978-3-319-58838-4_1', 'ranking-for-class-imbalance'),
    ('10.1109/IJCNN.2016.7727469', 'ranking-for-class-imbalance'),
]
my_categories = [  # for purposes of SJR Quantile Rank
    'Applied Mathematics', 'Artificial Intelligence', 'Bioengineering',
    'Biomedical Engineering', 'Computational Mathematics',
    'Computer Science Applications', 'Computer Science (miscellaneous)',
    'Computer Vision and Pattern Recognition', 'Control and Optimization',
    'Electrical and Electronic Engineering', 'Engineering (miscellaneous)',
    'Mathematics (miscellaneous)', 'Signal Processing',
    'Statistics and Probability', 'Statistics, Probability and Uncertainty',
]

table = [papers.get_paper_info(*p, my_categories) for p in tqdm(table)]

h_index = sum(i+1 <= paper['Citations'] for i, paper in enumerate(sorted(table, key=lambda x: x['Citations'], reverse=True)))

if args.type == 'latex':
    out.section('section-scientific-impact', 'Scientific Impact')
    # split papers into types and reduce columns
    for type in sorted(set([p['Type'] for p in table])):
        out.section('section-publications', f'{type.replace("-", " ").title()} Publications')
        keys = ['Year', 'Paper', 'Citations']
        if type in ('journal-article', 'book-chapter'):
            keys.append('SJR Rank')
        else:
            keys.append('CORE Rank')
        subtable = [{k: p[k] for k in keys} for p in table if p['Type'] == type]
        out.table(subtable, [], [], [], (None, '25em', None, None))
else:  # html
    out.section('section-publications', 'Publications')
    out.paragraph(f'Crossref h-index: {h_index}')
    out.table(table, ['Topic', 'Type'], ["int", "str", "str", "str", "int", "str", "str"], ["desc", None, None, None, "desc", "asc", "asc"])

################################## AWARDS ##################################

out.section('section-awards', 'Awards')
out.description([
    ('2022', '[Bosch for Mobility:](https://noticias.up.pt/estudantes-da-u-porto-brilham-em-concurso-de-conducao-autonoma-da-bosch/) My students won Best New Participating Team in an autonomous driving competition'),
    ('2021', '[INESC TEC Outstanding Recognition Award:](https://bip.inesctec.pt/en/especiaisdecorrida/ricardo-cruz-ctm-2/) INESC TEC internal award, reason: maintenance of the HPC infrastructure'),
    ('2021', 'Pedagogic award (voted by students): University of Porto (FEUP)'),
    ('2021', '[Best paper and presentation:](https://noticias.up.pt/investigadores-da-u-porto-dominam-premios-do-recpad-2021/) RECPAD national conference'),
    ('2018', '[INESC TEC Outstanding Recognition Award:](http://bip-archive.inesctec.pt/en/196/fora-de-serie.html) INESC TEC internal award, reason: help organizing workshops'),
    ('2017', 'Kaggle Bronze Medal (competition) and Silver (engagement)'),
])

################################ SUPERVISIONS ################################

table = [
    {'Year': 'on-going', 'Degree': 'MSc', 'Student': 'Diana Teixeira Silva', 'Co-supervisor(s)': '', 'Thesis/Project': 'Quantifying How Deep Implicit Representations Promote Label Efficiency', 'University': 'FEUP'},
    {'Year': 'on-going', 'Degree': 'MSc', 'Student': 'Francisco Gonçalves Cerqueira', 'Co-supervisor(s)': '', 'Thesis/Project': 'Comparative Study on Self-Supervision Methods for Autonomous Driving', 'University': 'FEUP'},
    {'Year': 2024, 'Degree': 'MSc', 'Student': 'Airton Tiago', 'Co-supervisor(s)': 'Jaime Cardoso', 'Thesis/Project': 'Data Augmentation for Ordinal Data', 'University': 'FEUP'},
    {'Year': 2023, 'Degree': 'MSc', 'Student': 'Alankrita Asthana', 'Co-supervisor(s)': '', 'Thesis/Project': 'Iterative Inference for Point-Clouds', 'University': 'TUM'},
    {'Year': 2023, 'Degree': 'MSc', 'Student': 'Rafael Cristino', 'Co-supervisor(s)': 'Jaime Cardoso', 'Thesis/Project': '[Introducing Domain Knowledge to Scene Parsing in Autonomous Driving](https://repositorio-aberto.up.pt/handle/10216/152109)', 'University': 'FEUP'},
    {'Year': 2023, 'Degree': 'MSc', 'Student': 'José Guerra', 'Co-supervisor(s)': 'Luís Teixeira', 'Thesis/Project': '[Uncertainty-Driven Out-of-Distribution Detection in 3D LiDAR Object Detection for Autonomous Driving](https://repositorio-aberto.up.pt/handle/10216/152016) (Internship at Bosch Car Multimedia)', 'University': 'FEUP'},
    {'Year': 2022, 'Degree': 'MSc', 'Student': 'Pedro Silva', 'Co-supervisor(s)': 'Tiago Gonçalves', 'Thesis/Project': '[Human Feedback during Neural Networks Training](https://repositorio-aberto.up.pt/handle/10216/142444)', 'University': 'FEUP'},
    {'Year': 2022, 'Degree': 'MSc', 'Student': 'João Silva', 'Co-supervisor(s)': '', 'Thesis/Project': '[Environment Detection for Railway Applications based on Automotive Technology](https://repositorio-aberto.up.pt/handle/10216/142326) (Internship at Continental)', 'University': 'FEUP'},
    {'Year': 2022, 'Degree': 'MSc', 'Student': 'Ana Bezerra', 'Co-supervisor(s)': 'Joaquim Costa', 'Thesis/Project': '[Phishing Detection with a Machine Learning Net](https://repositorio-aberto.up.pt/handle/10216/147350) (Internship at E-goi)', 'University': 'FCUP'},
    {'Year': 2024, 'Degree': 'BSc', 'Student': 'Eliandro Melo', 'Co-supervisor(s)': '', 'Thesis/Project': 'Resource Efficiency using Deep Q-Learning in Autonomous Driving', 'University': 'FCUP'},
    {'Year': 2024, 'Degree': 'BSc', 'Student': 'Ivo Duarte Simões', 'Co-supervisor(s)': '', 'Thesis/Project': 'Resource Efficiency using PPO in Autonomous Driving', 'University': 'FCUP'},
    {'Year': 2023, 'Degree': 'BSc', 'Student': 'Diana Teixeira Silva', 'Co-supervisor(s)': '', 'Thesis/Project': 'Condition Invariance for Autonomous Driving by Adversarial Learning', 'University': 'FEUP'},
    {'Year': 2022, 'Degree': 'BSc', 'Student': 'Diana Teixeira Silva', 'Co-supervisor(s)': 'Tiago Gonçalves', 'Thesis/Project': 'Semantic Segmentation in Neural Networks using Iterative Visual Attention', 'University': 'FEUP'},
    {'Year': 2022, 'Degree': 'BSc', 'Student': 'Filipe Campos, Francisco Cerqueira, Vasco Alves', 'Co-supervisor(s)': '', 'Thesis/Project': '[Mobile App using Object Detection for Car Driving](https://play.google.com/store/apps/details?id=pt.up.fe.mobilecardriving)', 'University': 'FEUP'},
    {'Year': 2022, 'Degree': 'BSc', 'Student': 'Bruno Gomes, Rafael Camelo', 'Co-supervisor(s)': '', 'Thesis/Project': 'Internship at ANO', 'University': 'FEUP'},
]

if args.type == 'latex':
    # split supervisions into types and reduce columns
    for degree in ['MSc', 'BSc']:
        out.section('section-supervisions', f'{degree} Supervisions')
        type = 'Thesis' if 'MSc' else 'Project'
        rename_keys = {'Year': 'Year', 'Student': 'Student', 'Thesis/Project': type}
        subtable = [{rename_keys[k]: row[k] for k in rename_keys} for row in table if row['Degree'] == degree]
        out.table(subtable, [], [], [], (None, '10em', '25em'))
else:  # html
    out.section('section-supervisions', 'Supervisions')
    out.table(table, ['Degree'], ["str", "str", None, None, None, "str"], ["desc", "desc", None, None, None, "asc"])

##################################### END #####################################

out.paragraph(f'Last update: {datetime.now().strftime("%Y-%m-%d")}')
out.end()
