import argparse
parser = argparse.ArgumentParser()
parser.add_argument('type', choices=['html', 'latex'])
args = parser.parse_args()

from tqdm import tqdm
import datetime
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

table = [  # listed in publishing order
    ('10.1109/TIV.2024.3387113', 'applications'),
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
my_categories = frozenset((  # for purposes of SJR Quartile Rank
    'Applied Mathematics', 'Artificial Intelligence', 'Bioengineering',
    'Biomedical Engineering', 'Computational Mathematics',
    'Computer Science Applications', 'Computer Science (miscellaneous)',
    'Computer Vision and Pattern Recognition', 'Control and Optimization',
    'Electrical and Electronic Engineering', 'Engineering (miscellaneous)',
    'Mathematics (miscellaneous)', 'Signal Processing',
    'Statistics and Probability', 'Statistics, Probability and Uncertainty',
))

table = [papers.get_paper_info(*p, my_categories) for p in tqdm(table)]
count = {}
for p in table:
    count[p[3]] = count.get(p[3], 0)+1

manual_papers = [
    [2024, '==**[SUBMITTED]**== A Case Study on Phishing Detection with a Machine Learning Net\nA. Bezerra, I. Pereira, M. Ângelo, D. Coelho, D. Oliveira, J. Costa, **R. Cruz**\n*International Journal of Data Science and Analytics, Springer*', 'applications', 'journal'],
    [2024, '==**[SUBMITTED]**== Learning Ordinality in Semantic Segmentation\nR. Cristino, **R. Cruz**, J.Cardoso\n*Pattern Recognition, Elsevier*', 'ordinal-losses', 'journal'],
    [2024, '==**[SUBMITTED]**== Unimodal Distributions for Ordinal Regression\nJ. Cardoso, **R. Cruz**, T. Albuquerque\n*IEEE Transactions on Artificial Intelligence, IEEE*', 'ordinal-losses', 'journal'],
    # rejected :-(
    #[2024, '==**[SUBMITTED]**== Spatial Resource-Efficiency using Partial Convolutions for Segmentation and Object Detection\n**R. Cruz**\n*Pattern Recognition, Elsevier*', 'spatial-resource-efficiency', 'journal'],
    #[2024, '==**[SUBMITTED]**== CNN Explanation Methods for Ordinal Regression Tasks\nJ. Barbero-Gómez, **R. Cruz**, J. Cardoso, P. Gutiérrez, C. Hervás-Martínez\n*Pattern Recognition, Elsevier*', 'ordinal-losses', 'journal'],
]
for paper in manual_papers:
    venue = ' '.join(paper[1].split('\n')[-1][:-1].split()[:-1])[:-1]
    paper += ['']*4
    if paper[3] == 'journal':
        paper[5] = papers.get_impact_factor(venue)
        paper[6] = papers.get_sjr_rank(venue, my_categories)
    else:
        paper[7] = papers.get_core_rank(venue)

h_index = sum(i+1 <= paper[4] for i, paper in enumerate(sorted(table, key=lambda x: x[4], reverse=True)))
total_citations = sum(x[4] for x in table)
table = manual_papers + table
google_scholar_hindex = papers.get_scholar_hindex()

if args.type == 'latex':
    out.section('section-scientific-impact', 'Impact and Citations')
else:
    out.section('section-publications', 'Publications')
out.itemize([
    f'Google Scholar h-index: **{google_scholar_hindex}** ({datetime.datetime.now().strftime("%Y-%m-%d")})',
    f'Crossref h-index: **{h_index}** with **{total_citations}** total citations ({datetime.datetime.now().strftime("%Y-%m-%d")})',
    'Best oral paper: [2021 RECPAD conference](https://noticias.up.pt/investigadores-da-u-porto-dominam-premios-do-recpad-2021/)',
])
out.text(f"Sources (last update: {datetime.datetime.now().strftime('%Y-%m-%d')}): • Citation counts are from Crossref. • Impact Factor (IF) comes from each journal's webpage. • SJR rank quartiles are from Scimago and relate to the subject category closest to machine learning (not necessarily the best quartile). • CORE rank is from ICORE for whatever last year is available for that conference.")

columns = ['Year', 'Paper', 'Topic', 'Type', 'Citations', 'IF', 'SJR Rank', 'CORE Rank']
if args.type == 'latex':
    # split papers into types and reduce columns
    for type in ['journal', 'conference']:
        out.section('section-publications', f'{type.title()} Publications')
        ix = (0, 1, 4, 5) if type == 'journal' else (0, 1, 6)
        _columns = [columns[i] for i in ix]
        _table = [[row[i] for i in ix] for row in table if row[3] == type]
        size = '26em' if type == 'journal' else '28em'
        out.table(_table, _columns, None, [None, size] + [None]*(len(_columns)-2))
        out.text(f'Total {count[type]} {type} publications.' + (' (National conferences are omitted.)' if type == 'conference' else ''))
else:  # html
    out.table(table, columns, ['sort', 'text', 'filter', 'filter', 'sort', 'sort', 'sort', 'sort'], None)

################################ SUPERVISIONS ################################

table = [
    ('on-going', 'MSc', 'Diana Teixeira Silva', '', 'Quantifying How Deep Implicit Representations Promote Label Efficiency', 'FEUP'),
    ('on-going', 'MSc', 'Francisco Gonçalves Cerqueira', '', 'Comparative Study on Self-Supervision Methods for Autonomous Driving', 'FEUP'),
    (2024, 'MSc', 'Airton Tiago', 'Jaime Cardoso', '[Data Augmentation for Ordinal Data](https://repositorio-aberto.up.pt/handle/10216/157714)', 'FEUP'),
    (2023, 'MSc', 'Alankrita Asthana', '', 'Iterative Inference for Point-Clouds', 'TUM'),
    (2023, 'MSc', 'Rafael Cristino', 'Jaime Cardoso', '[Introducing Domain Knowledge to Scene Parsing in Autonomous Driving](https://repositorio-aberto.up.pt/handle/10216/152109)', 'FEUP'),
    (2023, 'MSc', 'José Guerra', 'Luís Teixeira', '[Uncertainty-Driven Out-of-Distribution Detection in 3D LiDAR Object Detection for Autonomous Driving](https://repositorio-aberto.up.pt/handle/10216/152016) (Internship at Bosch Car Multimedia)', 'FEUP'),
    (2022, 'MSc', 'Pedro Silva', 'Tiago Gonçalves', '[Human Feedback during Neural Networks Training](https://repositorio-aberto.up.pt/handle/10216/142444)', 'FEUP'),
    (2022, 'MSc', 'João Silva', '', '[Environment Detection for Railway Applications based on Automotive Technology](https://repositorio-aberto.up.pt/handle/10216/142326) (Internship at Continental)', 'FEUP'),
    (2022, 'MSc', 'Ana Bezerra', 'Joaquim Costa', '[Phishing Detection with a Machine Learning Net](https://repositorio-aberto.up.pt/handle/10216/147350) (Internship at E-goi)', 'FCUP'),
    ('on-going', 'BSc', 'João Monteiro', 'Celso Pereira', 'Cross-vehicle collaboration using RGB cameras', 'FCUP'),
    ('on-going', 'BSc', 'Diogo Mendes', 'Nuno Lavado', 'Automatic Recognition of Pig Activity in an Intensive Production System', 'FCUP'),
    ('on-going', 'BSc', 'Beatriz Sá', 'Jaime S. Cardoso', 'Research on Deep Augmentation for Ordinal Regression', 'FCUP'),
    (2024, 'BSc', 'Eliandro Melo', '', 'Resource Efficiency using Deep Q-Learning in Autonomous Driving', 'FCUP'),
    (2024, 'BSc', 'Ivo Duarte Simões', '', 'Resource Efficiency using PPO in Autonomous Driving', 'FCUP'),
    (2023, 'BSc', 'Diana Teixeira Silva', '', 'Condition Invariance for Autonomous Driving by Adversarial Learning', 'FEUP'),
    (2022, 'BSc', 'Diana Teixeira Silva', 'Tiago Gonçalves', 'Semantic Segmentation in Neural Networks using Iterative Visual Attention', 'FEUP'),
    (2022, 'BSc', 'Filipe Campos, Francisco Cerqueira, Vasco Alves', '', '[Mobile App using Object Detection for Car Driving](https://play.google.com/store/apps/details?id=pt.up.fe.mobilecardriving)', 'FEUP'),
    (2022, 'BSc', 'Bruno Gomes, Rafael Camelo', '', 'Internship at ANO', 'FEUP'),
]

if args.type == 'latex':
    # split supervisions into types and reduce columns
    ix = (0, 2, 4, 5)
    for degree in ['MSc', 'BSc']:
        out.section('section-supervisions', f'{degree} Supervisions')
        columns = ['Year', 'Student', 'Dissertation' if degree == 'MSc' else 'Project', 'University']
        _table = [[row[i] for i in ix] for row in table if row[1] == degree]
        out.table(_table, columns, None, [None, '7em', '18.5em', None])
else:  # html
    columns = ['Year', 'Degree', 'Student', 'Co-supervisor(s)', 'Dissertation/Project', 'University']
    out.section('section-supervisions', 'Supervisions')
    out.table(table, columns, ['sort', 'filter', 'text', 'sort'], None)

############################# JURY PARTICIPATION #############################

items = (
    ('2023/12', 'External Examiner @ U.Minho: MSc Dissertation "Prediction System for Municipal Waste Containers"'),
    ('2023/07', 'Examiner @ INESC TEC: Evaluation of 6 summer interships (SCI 2023) on computer vision and machine learning'),
    ('2022/10', 'External Examiner @ FEUP: MSc Dissertation "Neuroblastoma Cancer Radiogenomics"'),
    ('2022/10', 'External Examiner @ FEUP: MSc Dissertation "AI-Based Models to Predict The Traumatic Brain Injury Outcome"'),
    ('2022/07', 'Examiner @ INESC TEC: Evaluation of 2 summer interships (SCI 2022) on computer vision and machine learning'),
    ('2022/07', 'Chairman @ FEUP: MSc Dissertation "Learning to write medical reports from EEG data"'),
    ('2022/07', 'External Examiner @ U.Minho: MSc Dissertation "Detection and classification of small impacts on vehicles based on deep learning algorithms"'),
    ('2021/12', 'External Examiner @ FCUP: MSc Dissertation "3D Lung Computed Tomography Synthesis using Generative Adversarial Networks"'),
    ('2021/09', 'External Examiner @ U.Minho: MSc Dissertation "Feasibility of using autoencoders for learning car interior background models"'),
    ('2021/07', 'Examiner @ INESC TEC: Evaluation of 4 summer interships (SCI 2021) on computer vision and machine learning'),
)

if args.type == 'latex':
    out.section('section-jury-participation', f'Jury Participation')
    out.description(items)

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
    out.text(f'Last update: {datetime.datetime.now().strftime("%Y-%m-%d")}')
out.end()
