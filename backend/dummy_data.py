from app import create_app, db
from app.models.models import User, Program, Objective, Attribute, AttrObjRel, Observation, ModObsRel, Module, Material, Tag, Comment, Notification
from datetime import datetime

app = create_app()


def insert_data():
    # Users
    users = [
        User(username='系统管理员', password='admin', role='admin'),
        User(username='测试员A', password='test-a', role='auditor'),
        User(username='测试员B', password='test-b', role='staff'),
        User(username='测试员C', password='test-c', role='staff'),
        User(username='测试员D', password='test-d', role='guest'),
    ]

    # Programs
    programs = [
        Program(name='软件工程专业（嵌入式培养）人才培养方案', description='本专业坚持立德树人，培养“德、智、体、美、劳”全面发展，具有适应软件系统开发、软件工程服务和技术研究等所需的数学与自然科学基础知识、软件工程学科基础理论；具有终身学习、创新能力、外语运用能力、团队合作能力和沟通交流能力等良好的素养；能够承担复杂软件系统的开发、应用、测试、维护等任务，适应长三角地区软件与信息技术服务业发展需求的应用型软件工程人才。毕业学生能在企事业、行政管理部门等单位从事软件系统（包括软件服务外包）开发、软件工程服务和技术研究与管理等工作。', version='2018版 适用2019、2020级')
    ]

    # Objectives
    objectives = [
        Objective(
            name='目标1', description='具有良好的社会与职业道德，社会和环境意识强，具有担当精神和较强的责任心。', program_id=1),
        Objective(
            name='目标2', description='具有扎实的数理知识、专业基础理论和专业技能，具有良好的学科素养和工程开发能力，能有效运用工程知识和技术原理，解决软件工程领域的复杂工程问题。', program_id=1),
        Objective(
            name='目标3', description='具备一定的创新能力、外语运用能力、团队合作能力和沟通交流能力。', program_id=1),
        Objective(
            name='目标4', description='能够在软件工程相关领域担任产品经理、软件开发工程师、软件测试工程师、项目经理、软件服务咨询师、技术支持工程师等工作。', program_id=1),
        Objective(
            name='目标5', description='具有终身学习的意识与能力，紧跟软件工程领域的技术进步，具备职业可持续发展的潜能，并能够胜任其他领域与软件工程相关的工作。', program_id=1),
    ]

    # Attributes
    attributes = [
        Attribute(
            name='工程知识', description='能够将数学、自然科学、计算机学科基础、软件工程基础和专业知识用于解决复杂软件工程问题。', program_id=1),
        Attribute(
            name='问题分析', description='能够应用数学、自然科学和工程科学的基本原理，识别、表达、并通过文献研究分析软件工程专业的复杂工程问题，以获得有效结论。', program_id=1),
        Attribute(name='设计/开发解决方案', description='能够设计针对软件工程领域复杂工程问题的解决方案，设计满足特定需求的软件系统或组件，并能够在设计开发环节中体现创新意识， 考虑社会、健康、安全、法律、文化以及环境等因素。', program_id=1),
        Attribute(
            name='研究', description='能够基于科学原理并采用科学方法对软件领域的复杂工程问题进行研究，包括设计实验、分析与解释数据、并通过信息综合得到合理有效的结论。 ', program_id=1),
    ]

    # AttrObjRel
    attr_obj_rels = [
        AttrObjRel(attribute_id=1, objective_id=2, weight=1),
        AttrObjRel(attribute_id=2, objective_id=2, weight=1),
        AttrObjRel(attribute_id=3, objective_id=1, weight=1),
        AttrObjRel(attribute_id=3, objective_id=2, weight=1),
        AttrObjRel(attribute_id=3, objective_id=3, weight=1),
        AttrObjRel(attribute_id=3, objective_id=5, weight=1),
    ]

    # Observations
    observations = [
        Observation(
            name='指标点1-1', description='能将数学、物理、计算机学科基础及软件工程学科的相关知识用于软件工程领域复杂工程问题的表述', attribute_id=1),
        Observation(name='指标点1-2',
                    description='能针对计算机软、硬件系统具体问题建立数学模型并求解', attribute_id=1),
        Observation(
            name='指标点1-3', description='能够将软件领域的相关知识和数学模型方法用于推理、分析复杂软件工程问题', attribute_id=1),
        Observation(
            name='指标点1-4', description='能够将软件领域的相关知识和数学模型方法用于复杂软件工程问题解决方案的比较与综合', attribute_id=1),
    ]

    # Modules
    modules = [
        Module(name='高等数学A（上）', name_en='Advanced Mathematics A (I)', nature='通识教育课程', category='必修', number='0801001',
               credit=5.0, lec_hours=80, lab_hours=0, oncampus_prac=0, offcampus_prac=0, term='一', description='', program_id=1),
        Module(name='线性代数', name_en='Linear Algebra', nature='专业基础课程', category='必修', number='0801008', credit=2.0,
               lec_hours=32, lab_hours=0, oncampus_prac=0, offcampus_prac=0, term='一', description='', program_id=1),
        Module(name='数据结构', name_en='Data Structure', nature='专业基础课程', category='必修', number='0300003', credit=4.0,
               lec_hours=48, lab_hours=16, oncampus_prac=0, offcampus_prac=0, term='三', description='', program_id=1),
        Module(name='体育Ⅴ', name_en='Physical Education Ⅴ', nature='通识教育课程', category='必修', number='1103010', credit=0.5,
               lec_hours=0, lab_hours=0, oncampus_prac=0, offcampus_prac=18, term='五', description='', program_id=1),
    ]

    # ModObsRel
    mod_obs_rels = [
        ModObsRel(module_id=2, observation_id=1, weight=1),
        ModObsRel(module_id=3, observation_id=3, weight=1),
    ]

    # Materials
    materials = [
        Material(title='2022-2023-2试卷命题审核表', description='', file_path='tmp/aa.pdf', created_at=datetime.strptime('2023-10-23',
                 '%Y-%m-%d'), updated_at=datetime.strptime('2023-10-23', '%Y-%m-%d'), user_id=3, module_id=2, tag_id=1),
        Material(title='2022-2023-2考核合理性审核表', description='', file_path='tmp/ab.pdf', created_at=datetime.strptime('2023-10-26',
                 '%Y-%m-%d'), updated_at=datetime.strptime('2023-10-26', '%Y-%m-%d'), user_id=4, module_id=3, tag_id=2),
        Material(title='2022-2023-2计划进度表', description='', file_path='tmp/ac.pdf', created_at=datetime.strptime('2023-10-26',
                 '%Y-%m-%d'), updated_at=datetime.strptime('2023-10-26', '%Y-%m-%d'), user_id=4, module_id=3, tag_id=3),
        Material(title='2022-2023-2试卷命题审核表', description='', file_path='tmp/ad.pdf', created_at=datetime.strptime('2023-10-27',
                 '%Y-%m-%d'), updated_at=datetime.strptime('2023-11-01', '%Y-%m-%d'), user_id=4, module_id=3, tag_id=1),
    ]

    # Tags
    tags = [
        Tag(name='试卷命题审核表', user_id=2, created_at=datetime.strptime(
            '2023-06-30', '%Y-%m-%d')),
        Tag(name='考核合理性审核表', user_id=2,
            created_at=datetime.strptime('2023-06-30', '%Y-%m-%d')),
        Tag(name='计划进度表', user_id=2, created_at=datetime.strptime(
            '2023-07-14', '%Y-%m-%d')),
    ]

    # Comments
    comments = [
        Comment(text='格式有问题，请修改并更新附件', created_at=datetime.strptime(
            '2023-10-30', '%Y-%m-%d'), user_id=2, material_id=1),
        Comment(text='日期不对', created_at=datetime.strptime(
            '2023-10-30', '%Y-%m-%d'), user_id=2, material_id=3),
        Comment(text='我看错了，不用重做', created_at=datetime.strptime(
            '2023-10-31', '%Y-%m-%d'), user_id=2, material_id=3),
    ]

    # Notifications
    notifications = [
        Notification(message='【公告】请尽快上传教学材料', created_at=datetime.strptime(
            '2023-09-10', '%Y-%m-%d'), user_id=4),
        Notification(message='【通知】您的教学材料有一条新评论', created_at=datetime.strptime(
            '2023-10-31', '%Y-%m-%d'), user_id=4),
    ]

    with app.app_context():
        db.create_all()

        # Insert entity data
        db.session.add_all(users + programs)
        db.session.commit()
        print('users + programs')
        db.session.add_all(objectives + attributes + modules + notifications)
        db.session.commit()
        print('objectives + attributes + modules + notifications')
        db.session.add_all(observations + materials + tags)
        db.session.commit()
        print('observations + materials + tags')
        db.session.add_all(comments)
        db.session.commit()
        print('comments')

        # Insert relation data
        db.session.add_all(attr_obj_rels + mod_obs_rels)
        db.session.commit()
        print('attr_obj_rels + mod_obs_rels')


if __name__ == '__main__':
    insert_data()
