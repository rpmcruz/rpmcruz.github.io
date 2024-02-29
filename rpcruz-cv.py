import argparse
parser = argparse.ArgumentParser()
parser.add_argument('type', choices=['html', 'latex'])
args = parser.parse_args()

from tqdm import tqdm
from datetime import datetime
import sys
import papers, out

out = getattr(out, args.type.title())()

education = [
    ('2021 PhD', 'Computer Science (joint degree University of Porto, Minho and Aveiro)'),
    ('2015 M.Sc.', 'Mathematical Engineering (Faculty of Sciences, University of Porto)'),
    ('2012 B.Sc.', 'Computer Science (Faculty of Sciences, University of Porto)'),
]
employment = [
    ('2021/09--present', '**Post-doctoral Researcher** on Autonomous Driving\nUniversity of Porto (FEUP) [in partnership with Bosch]\n- Collaboration between the University of Porto and Bosch Car Multimedia to improve autonomous driving perception\n- Developed frameworks for object detection using camera and LiDAR (2D discretization and raw point-clouds)\n- Published new methods for efficient semantic segmentation and ordinal regression\n- Supervised six master’s theses, four bachelor’s projects, and other team members\n- Responsible for the HPC infrastructure (using Slurm)'),
    ('2023/09--2024/02', '**Invited Auxiliary Professor**, University of Porto (FEUP)\nCourses:\n- OAT4001 & FACVC: Machine Learning'),
    ('2021/09--2022/08', '**Invited Auxiliary Professor**, University of Porto (FEUP)\nCourses:\n- L.EIC003: Programming Fundamentals (Python)\n- L.EEC009: Data Structures and Algorithms (C/C++)'),
    ('2018/09--2021/08', '**Invited Teacher Assistant**, University of Porto (FEUP)\nCourses:\n- L.EIC003: Programming Fundamentals (Python)\n- L.EIC009: Programming (C/C++)'),
    ('2015/09--2021/08', '**Research Assistant** on Machine Learning and Computer Vision\nINESC TEC\n- Research focus: re-thinking fundamentals about image classification and semantic segmentation (8+ publications)\n- Some highlights: (1) a method for background invariance using adversarial training, (2) new losses that minimize absolute trade-offs between Type 1 and 2 errors instead of relative trade-offs, (3) using backpropagation also for inference to refine existing outputs, (4) deploying learning-to-rank methods for class imbalance\n- Contributed to workshops, Summer School on Computer Vision (VISUM), and other events\n- Twice awarded "outstanding recognition" for organizing workshops and helping with the HPC infrastructure'),
    ('2014/09--2014/12', '**Research Grant** on Mathematical Modelling Research\nMathematics Center of the University of Porto (CMUP)\n- Epidemiological models for HIV. A little of everything: from differential equations to stochastic simulations to cellular automata.'),
]

#################################### START ####################################

out.begin('Ricardo Cruz, PhD')
contacts = [
    ('profile-email', 'rpcruz@fe.up.pt', 'mailto:rpcruz@fe.up.pt'),
    ('profile-orcid', '0000-0002-5189-6228', 'https://orcid.org/0000-0002-5189-6228'),
    ('profile-github', 'github.com/rpmcruz', 'https://github.com/rpmcruz?tab=repositories'),
]
if args.type == 'latex':
    contacts.insert(1, ('profile-website', 'rpmcruz.github.io', 'https://rpmcruz.github.io/'))
else:  # html
    contacts.append(('profile-pdf', 'PDF', 'https://rpmcruz.github.io/rpcruz-cv.pdf'))

out.contacts(contacts)
out.text('Ricardo Cruz has worked on a wide range of machine learning topics, with particular emphasis on theoretical aspects of deep learning and computer vision -- with 20+ publications and 100+ citations in such topics as: • adapting ranking models for class imbalance; • making convolutional neural networks invariant to background; • making them faster by adjusting the computational effort to each image; • losses for ordinal regression. He is a Post-doc Researcher on autonomous driving at the Faculty of Engineering, University of Porto, and he has been a researcher at INESC TEC since 2015, where his research earned him the computer science PhD in 2021. He has a BSc in computer science and a MSc in applied mathematics. He is frequently invited to teach at the Faculty of Engineering, University of Porto, where he earned a pedagogic award.')

if args.type == 'latex':
    out.section('section-education', 'Education')
    out.description(education)
    out.section('section-employment', 'Employment')
    out.description(employment)

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

table = [
    {'Year': 2024, 'Paper': '==**[SUBMITTED]**== Weather and Meteorological Optical Range Classification for Autonomous Driving\nC. Pereira, J. Fernandes, **R. Cruz**, J. Pinto, J. Cardoso\n*IEEE Transactions on Intelligent Vehicles*', 'Topic': 'applications', 'Type': 'journal-article', 'Citations': 0, 'SJR Rank': 'Q1', 'CORE Rank': ''},
    {'Year': 2024, 'Paper': '==**[SUBMITTED]**== A Case Study on Phishing Detection with a Machine Learning Net\nA. Bezerra, I. Pereira, M. Ângelo, D. Coelho, D. Oliveira, J. Costa, **R. Cruz**\n*Springer International Journal of Data Science and Analytics*', 'Topic': 'applications', 'Type': 'journal-article', 'Citations': 0, 'SJR Rank': 'Q2', 'CORE Rank': ''},
    {'Year': 2024, 'Paper': '==**[SUBMITTED]**== Spatial Resource-Efficiency using Partial Convolutions for Segmentation and Object Detection\n**R. Cruz**\n*Elsevier Pattern Recognition*', 'Topic': 'spatial-resource-efficiency', 'Type': 'journal-article', 'Citations': 0, 'SJR Rank': 'Q1', 'CORE Rank': ''},
    {'Year': 2024, 'Paper': '==**[SUBMITTED]**== Learning Ordinality in Semantic Segmentation\nR. Cristino, **R. Cruz**, J.Cardoso\n*Elsevier Pattern Recognition*', 'Topic': 'ordinal-losses', 'Type': 'journal-article', 'Citations': 0, 'SJR Rank': 'Q1', 'CORE Rank': ''},
    #{'Year': 2024, 'Paper': '==**[SUBMITTED]**== CNN Explanation Methods for Ordinal Regression Tasks\nJ. Barbero-Gómez, **R. Cruz**, J. Cardoso, P. Gutiérrez, C. Hervás-Martínez\n*Elsevier Pattern Recognition*', 'Topic': 'ordinal-losses', 'Type': 'journal-article', 'Citations': 0, 'SJR Rank': 'Q1', 'CORE Rank': ''},
    {'Year': 2024, 'Paper': '==**[SUBMITTED]**== Unimodal Distributions for Ordinal Regression\nJ. Cardoso, **R. Cruz**, T. Albuquerque\n*IEEE Transactions on Artificial Intelligence*', 'Topic': 'ordinal-losses', 'Type': 'journal-article', 'Citations': 0, 'SJR Rank': 'Q1', 'CORE Rank': ''},
] + table

h_index = sum(i+1 <= paper['Citations'] for i, paper in enumerate(sorted(table, key=lambda x: x['Citations'], reverse=True)))
total_citations = sum(x['Citations'] for x in table)

if args.type == 'latex':
    out.section('section-scientific-impact', 'Impact and Citations')
else:
    out.section('section-publications', 'Publications')
out.itemize([
    f'Crossref h-index: **{h_index}** with **{total_citations}** total citations ({datetime.now().strftime("%Y-%m-%d")})',
    'Google Scholar h-index: **7** (2024-02)',
    'Best oral paper: [2021 RECPAD conference](https://noticias.up.pt/investigadores-da-u-porto-dominam-premios-do-recpad-2021/)',
])
out.text(f'The following citation counts come from Crossref. The SJR rank quantiles are of subject categories related to machine learning. The CORE rank is of the last year that is available for that conference. (last update: {datetime.now().strftime("%Y-%m-%d")})')

if args.type == 'latex':
    # split papers into types and reduce columns
    for title, type in [('Journal', 'journal-article'), ('Book Chapter', 'book-chapter'), ('Proceedings', 'proceedings-article')]:
        out.section('section-publications', f'{title} Publications')
        keys = ['Year', 'Paper', 'Citations']
        if type in ('journal-article', 'book-chapter'):
            keys.append('SJR Rank')
        else:
            keys.append('CORE Rank')
        subtable = [{k: p[k] for k in keys} for p in table if p['Type'] == type]
        out.table(subtable, [], [], [], (None, '25em', None, None))
else:  # html
    out.table(table, ['Topic', 'Type'], ["int", "str", "str", "str", "int", "str", "str"], ["desc", None, None, None, "desc", "asc", "asc"])

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
        type = 'Thesis' if degree == 'MSc' else 'Project'
        rename_keys = {'Year': 'Year', 'Student': 'Student', 'Thesis/Project': type}
        subtable = [{rename_keys[k]: row[k] for k in rename_keys} for row in table if row['Degree'] == degree]
        out.table(subtable, [], [], [], (None, '10em', '25em'))
else:  # html
    out.section('section-supervisions', 'Supervisions')
    out.table(table, ['Degree'], ["str", "str", None, None, None, "str"], ["desc", "desc", None, None, None, "asc"])

########################### EDUCATION & EMPLOYMENT ###########################

if args.type == 'html':
    out.section('section-education', 'Education')
    out.description(education)
    out.section('section-employment', 'Employment')
    out.description(employment)

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

##################################### END #####################################

if args.type == 'html':
    out.text(f'Last update: {datetime.now().strftime("%Y-%m-%d")}')
out.end()
