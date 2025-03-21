from datetime import datetime

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = 'user'  # type: ignore

    id: int | None = Field(default=None, primary_key=True, unique=True)
    surname: str = Field(max_length=45)
    name: str = Field(max_length=45)
    paternity: str | None = Field(max_length=45)
    gender: str | None = Field(max_length=45)
    birthdate: datetime | None = Field(default=None)
    login: str = Field(max_length=25, unique=True)
    password: str = Field(max_length=25)
    role_id: int = Field(foreign_key='role.id')


class Role(SQLModel, table=True):
    __tablename__ = 'role'  # type: ignore

    id: int | None = Field(default=None, primary_key=True, unique=True)
    name: str = Field(max_length=25)


class Group(SQLModel, table=True):
    __tablename__ = 'group'  # type: ignore

    id: int | None = Field(default=None, primary_key=True, unique=True)
    name: str = Field(max_length=25)


class UserGroup(SQLModel, table=True):
    __tablename__ = 'user_group'  # type: ignore

    id: int | None = Field(default=None, primary_key=True, unique=True)
    user_id: int = Field(foreign_key='user.id')
    group_id: int = Field(foreign_key='group.id')


class Cabinet(SQLModel, table=True):
    __tablename__ = 'cabinet'  # type: ignore

    id: int | None = Field(default=None, primary_key=True, unique=True)
    description: str = Field(max_length=45)


class Subject(SQLModel, table=True):
    __tablename__ = 'subject'  # type: ignore

    id: int | None = Field(default=None, primary_key=True, unique=True)
    name: str = Field(max_length=50)
    description: str = Field(max_length=50)
    type: str = Field(max_length=50)


class Schedule(SQLModel, table=True):
    __tablename__ = 'schedule'  # type: ignore

    id: int | None = Field(default=None, primary_key=True, unique=True)
    dateandtime: datetime = Field(default_factory=datetime.now)
    teacher_id: int = Field(foreign_key='user.id')


class ScheduleSubject(SQLModel, table=True):
    __tablename__ = 'schedule_subject'  # type: ignore

    id: int | None = Field(default=None, primary_key=True, unique=True)
    schedule_id: int = Field(foreign_key='schedule.id')
    subject_id: int = Field(foreign_key='subject.id')


class ScheduleCabinet(SQLModel, table=True):
    __tablename__ = 'schedule_cabinet'  # type: ignore

    id: int | None = Field(default=None, primary_key=True, unique=True)
    schedule_id: int = Field(foreign_key='schedule.id')
    cabinet_id: int = Field(foreign_key='cabinet.id')
