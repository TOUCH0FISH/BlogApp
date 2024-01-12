from datetime import datetime
from ..database import db


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(
        db.Enum('admin', 'staff', 'auditor', 'guest'), nullable=False)

    def serialize(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'role': self.role
        }

    def __repr__(self):
        return f'<User {self.username}>'


class Program(db.Model):
    __tablename__ = 'program'
    program_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    version = db.Column(db.String)
    # Relationships
    attributes = db.relationship('Attribute', backref='program', lazy=True)
    objectives = db.relationship('Objective', backref='program', lazy=True)
    modules = db.relationship('Module', backref='program', lazy=True)

    def __repr__(self):
        return f'<Program {self.name}>'


class Objective(db.Model):
    __tablename__ = 'objective'
    objective_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    program_id = db.Column(db.Integer, db.ForeignKey(
        'program.program_id'), nullable=False)

    def __repr__(self):
        return f'<Objective {self.name}>'


class Attribute(db.Model):
    __tablename__ = 'attribute'
    attribute_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    program_id = db.Column(db.Integer, db.ForeignKey(
        'program.program_id'), nullable=False)
    observations = db.relationship(
        'Observation', backref='attribute', lazy=True)

    def __repr__(self):
        return f'<Attribute {self.name}>'


class AttrObjRel(db.Model):
    __tablename__ = 'attrobjrel'
    attr_obj_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attribute_id = db.Column(db.Integer, db.ForeignKey(
        'attribute.attribute_id'), nullable=False)
    objective_id = db.Column(db.Integer, db.ForeignKey(
        'objective.objective_id'), nullable=False)
    weight = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<AttrObjRel {self.attr_obj_id}>'


class Observation(db.Model):
    __tablename__ = 'observation'
    observation_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    attribute_id = db.Column(db.Integer, db.ForeignKey(
        'attribute.attribute_id'), nullable=False)

    def __repr__(self):
        return f'<Observation {self.name}>'


class Module(db.Model):
    __tablename__ = 'module'
    module_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    name_en = db.Column(db.String)
    nature = db.Column(db.String)
    category = db.Column(db.String)
    number = db.Column(db.String)
    credit = db.Column(db.Numeric)
    lec_hours = db.Column(db.Integer)
    lab_hours = db.Column(db.Integer)
    oncampus_prac = db.Column(db.Integer)
    offcampus_prac = db.Column(db.Integer)
    term = db.Column(db.String)
    offered_by = db.Column(db.String)
    description = db.Column(db.Text)
    program_id = db.Column(db.Integer, db.ForeignKey(
        'program.program_id'), nullable=False)
    materials = db.relationship('Material', backref='module', lazy=True)

    def __repr__(self):
        return f'<Module {self.name}>'


class ModObsRel(db.Model):
    __tablename__ = 'modobsrel'
    mod_obs_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    module_id = db.Column(db.Integer, db.ForeignKey(
        'module.module_id'), nullable=False)
    observation_id = db.Column(db.Integer, db.ForeignKey(
        'observation.observation_id'), nullable=False)
    weight = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<ModObsRel {self.mod_obs_id}>'


class Tag(db.Model):
    __tablename__ = 'tag'
    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Tag {self.name}>'


class Material(db.Model):
    __tablename__ = 'material'
    material_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey(
        'module.module_id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.tag_id'), nullable=False)

    def __repr__(self):
        return f'<Material {self.title}>'


class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey(
        'material.material_id'), nullable=False)

    def serialize(self):
        return {
            'comment_id': self.comment_id,
            'text': self.text,
            'created_at': self.created_at.isoformat(),
            'user_id': self.user_id,
            'material_id': self.material_id
        }

    def __repr__(self):
        return f'<Comment {self.comment_id}>'


class Notification(db.Model):
    __tablename__ = 'notification'
    notification_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id'), nullable=False)  # Receiver of the Notification

    def serialize(self):
        return {
            'notification_id': self.notification_id,
            'message': self.message,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f'<Notification {self.notification_id}>'
