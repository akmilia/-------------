# from sqlmodel import Field, SQLModel

from datetime import datetime
from typing import List # type: ignore

from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

# Настройка базы данных
DATABASE_URL = "sqlite:///./diplom_school.db"
engine = create_engine(DATABASE_URL, echo=True)

# Создание таблиц в базе данных
SQLModel.metadata.create_all(engine)

# Инициализация FastAPI
app = FastAPI()

# Модели
class User(SQLModel, table=True):
    __tablename__ = 'user'  # type: ignore

    id: int | None = Field(default=None, primary_key=True, unique=True)
    surname: str = Field(max_length=45)
    name: str = Field(max_length=45)
    paternity: str = Field(max_length=45)
    gender: str = Field(max_length=45)
    birthdate: datetime = Field(default=None)
    login: str = Field(max_length=25, unique=True)
    password: str = Field(max_length=25)
    role_id: int = Field(foreign_key='role.id')


class Role(SQLModel, table=True):
    __tablename__ = 'role'  # type: ignore

    id: int = Field(default=None, primary_key=True, unique=True)
    name: str = Field(max_length=25)


class Group(SQLModel, table=True):
    __tablename__ = 'group'  # type: ignore

    id: int = Field(default=None, primary_key=True, unique=True)
    name: str = Field(max_length=25)


class UserGroup(SQLModel, table=True):
    __tablename__ = 'user_group'  # type: ignore

    id: int = Field(default=None, primary_key=True, unique=True)
    user_id: int = Field(foreign_key='user.id')
    group_id: int = Field(foreign_key='group.id')


class Cabinet(SQLModel, table=True):
    __tablename__ = 'cabinet'  # type: ignore

    id: int = Field(default=None, primary_key=True, unique=True)
    description: str = Field(max_length=45)


class Subject(SQLModel, table=True):
    __tablename__ = 'subject'  # type: ignore

    id: int = Field(default=None, primary_key=True, unique=True)
    name: str = Field(max_length=50)
    description: str = Field(max_length=50)
    type: str = Field(max_length=50)


class Schedule(SQLModel, table=True):
    __tablename__ = 'schedule'  # type: ignore

    id: int = Field(default=None, primary_key=True, unique=True)
    dateandtime: datetime = Field(default_factory=datetime.now)
    teacher_id: int = Field(foreign_key='user.id')


class ScheduleSubject(SQLModel, table=True):
    __tablename__ = 'schedule_subject'  # type: ignore

    id: int = Field(default=None, primary_key=True, unique=True)
    schedule_id: int = Field(foreign_key='schedule.id')
    subject_id: int = Field(foreign_key='subject.id')


class ScheduleCabinet(SQLModel, table=True):
    __tablename__ = 'schedule_cabinet'  # type: ignore

    id: int = Field(default=None, primary_key=True, unique=True)
    schedule_id: int = Field(foreign_key='schedule.id')
    cabinet_id: int = Field(foreign_key='cabinet.id')

# CRUD операции для User
@app.post("/users/", response_model=User)
def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@app.get("/users/", response_model=List[User]) # type: ignore 
def read_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users


@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User):
    with Session(engine) as session:
        db_user = session.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        user_data = user.model_dump(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_user, key, value)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()
        return {"message": "User deleted"}

# CRUD операции для Role
@app.post("/roles/", response_model=Role)
def create_role(role: Role):
    with Session(engine) as session:
        session.add(role)
        session.commit()
        session.refresh(role)
        return role


@app.get("/roles/", response_model=List[Role])  # type: ignore
def read_roles():
    with Session(engine) as session:
        roles = session.exec(select(Role)).all()
        return roles


@app.get("/roles/{role_id}", response_model=Role)
def read_role(role_id: int):
    with Session(engine) as session:
        role = session.get(Role, role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        return role


@app.put("/roles/{role_id}", response_model=Role)
def update_role(role_id: int, role: Role):
    with Session(engine) as session:
        db_role = session.get(Role, role_id)
        if not db_role:
            raise HTTPException(status_code=404, detail="Role not found")
        role_data = role.model_dump(exclude_unset=True)
        for key, value in role_data.items():
            setattr(db_role, key, value)
        session.add(db_role)
        session.commit()
        session.refresh(db_role)
        return db_role


@app.delete("/roles/{role_id}")
def delete_role(role_id: int):
    with Session(engine) as session:
        role = session.get(Role, role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        session.delete(role)
        session.commit()
        return {"message": "Role deleted"}

# CRUD операции для Group
@app.post("/groups/", response_model=Group)
def create_group(group: Group):
    with Session(engine) as session:
        session.add(group)
        session.commit()
        session.refresh(group)
        return group


@app.get("/groups/", response_model=List[Group]) # type: ignore
def read_groups():
    with Session(engine) as session:
        groups = session.exec(select(Group)).all()
        return groups


@app.get("/groups/{group_id}", response_model=Group)
def read_group(group_id: int):
    with Session(engine) as session:
        group = session.get(Group, group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        return group


@app.put("/groups/{group_id}", response_model=Group)
def update_group(group_id: int, group: Group):
    with Session(engine) as session:
        db_group = session.get(Group, group_id)
        if not db_group:
            raise HTTPException(status_code=404, detail="Group not found")
        group_data = group.model_dump(exclude_unset=True)
        for key, value in group_data.items():
            setattr(db_group, key, value)
        session.add(db_group)
        session.commit()
        session.refresh(db_group)
        return db_group


@app.delete("/groups/{group_id}")
def delete_group(group_id: int):
    with Session(engine) as session:
        group = session.get(Group, group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        session.delete(group)
        session.commit()
        return {"message": "Group deleted"}

# CRUD операции для UserGroup
@app.post("/user_groups/", response_model=UserGroup)
def create_user_group(user_group: UserGroup):
    with Session(engine) as session:
        session.add(user_group)
        session.commit()
        session.refresh(user_group)
        return user_group


@app.get("/user_groups/", response_model=List[UserGroup]) # type: ignore
def read_user_groups():
    with Session(engine) as session:
        user_groups = session.exec(select(UserGroup)).all()
        return user_groups


@app.get("/user_groups/{user_group_id}", response_model=UserGroup)
def read_user_group(user_group_id: int):
    with Session(engine) as session:
        user_group = session.get(UserGroup, user_group_id)
        if not user_group:
            raise HTTPException(status_code=404, detail="UserGroup not found")
        return user_group


@app.put("/user_groups/{user_group_id}", response_model=UserGroup)
def update_user_group(user_group_id: int, user_group: UserGroup):
    with Session(engine) as session:
        db_user_group = session.get(UserGroup, user_group_id)
        if not db_user_group:
            raise HTTPException(status_code=404, detail="UserGroup not found")
        user_group_data = user_group.model_dump(exclude_unset=True)
        for key, value in user_group_data.items():
            setattr(db_user_group, key, value)
        session.add(db_user_group)
        session.commit()
        session.refresh(db_user_group)
        return db_user_group


@app.delete("/user_groups/{user_group_id}")
def delete_user_group(user_group_id: int):
    with Session(engine) as session:
        user_group = session.get(UserGroup, user_group_id)
        if not user_group:
            raise HTTPException(status_code=404, detail="UserGroup not found")
        session.delete(user_group)
        session.commit()
        return {"message": "UserGroup deleted"}

# CRUD операции для Cabinet
@app.post("/cabinets/", response_model=Cabinet)
def create_cabinet(cabinet: Cabinet):
    with Session(engine) as session:
        session.add(cabinet)
        session.commit()
        session.refresh(cabinet)
        return cabinet


@app.get("/cabinets/", response_model=List[Cabinet]) # type: ignore
def read_cabinets():
    with Session(engine) as session:
        cabinets = session.exec(select(Cabinet)).all()
        return cabinets


@app.get("/cabinets/{cabinet_id}", response_model=Cabinet)
def read_cabinet(cabinet_id: int):
    with Session(engine) as session:
        cabinet = session.get(Cabinet, cabinet_id)
        if not cabinet:
            raise HTTPException(status_code=404, detail="Cabinet not found")
        return cabinet


@app.put("/cabinets/{cabinet_id}", response_model=Cabinet)
def update_cabinet(cabinet_id: int, cabinet: Cabinet):
    with Session(engine) as session:
        db_cabinet = session.get(Cabinet, cabinet_id)
        if not db_cabinet:
            raise HTTPException(status_code=404, detail="Cabinet not found")
        cabinet_data = cabinet.model_dump(exclude_unset=True)
        for key, value in cabinet_data.items():
            setattr(db_cabinet, key, value)
        session.add(db_cabinet)
        session.commit()
        session.refresh(db_cabinet)
        return db_cabinet


@app.delete("/cabinets/{cabinet_id}")
def delete_cabinet(cabinet_id: int):
    with Session(engine) as session:
        cabinet = session.get(Cabinet, cabinet_id)
        if not cabinet:
            raise HTTPException(status_code=404, detail="Cabinet not found")
        session.delete(cabinet)
        session.commit()
        return {"message": "Cabinet deleted"}

# CRUD операции для Subject
@app.post("/subjects/", response_model=Subject)
def create_subject(subject: Subject):
    with Session(engine) as session:
        session.add(subject)
        session.commit()
        session.refresh(subject)
        return subject


@app.get("/subjects/", response_model=List[Subject])# type: ignore
def read_subjects():
    with Session(engine) as session:
        subjects = session.exec(select(Subject)).all()
        return subjects


@app.get("/subjects/{subject_id}", response_model=Subject)
def read_subject(subject_id: int):
    with Session(engine) as session:
        subject = session.get(Subject, subject_id)
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        return subject


@app.put("/subjects/{subject_id}", response_model=Subject)
def update_subject(subject_id: int, subject: Subject):
    with Session(engine) as session:
        db_subject = session.get(Subject, subject_id)
        if not db_subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        subject_data = subject.model_dump(exclude_unset=True)
        for key, value in subject_data.items():
            setattr(db_subject, key, value)
        session.add(db_subject)
        session.commit()
        session.refresh(db_subject)
        return db_subject


@app.delete("/subjects/{subject_id}")
def delete_subject(subject_id: int):
    with Session(engine) as session:
        subject = session.get(Subject, subject_id)
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        session.delete(subject)
        session.commit()
        return {"message": "Subject deleted"}

# CRUD операции для Schedule
@app.post("/schedules/", response_model=Schedule)
def create_schedule(schedule: Schedule):
    with Session(engine) as session:
        session.add(schedule)
        session.commit()
        session.refresh(schedule)
        return schedule


@app.get("/schedules/", response_model=List[Schedule]) # type: ignore
def read_schedules():
    with Session(engine) as session:
        schedules = session.exec(select(Schedule)).all()
        return schedules


@app.get("/schedules/{schedule_id}", response_model=Schedule)
def read_schedule(schedule_id: int):
    with Session(engine) as session:
        schedule = session.get(Schedule, schedule_id)
        if not schedule:
            raise HTTPException(status_code=404, detail="Schedule not found")
        return schedule


@app.put("/schedules/{schedule_id}", response_model=Schedule)
def update_schedule(schedule_id: int, schedule: Schedule):
    with Session(engine) as session:
        db_schedule = session.get(Schedule, schedule_id)
        if not db_schedule:
            raise HTTPException(status_code=404, detail="Schedule not found")
        schedule_data = schedule.model_dump(exclude_unset=True)
        for key, value in schedule_data.items():
            setattr(db_schedule, key, value)
        session.add(db_schedule)
        session.commit()
        session.refresh(db_schedule)
        return db_schedule


@app.delete("/schedules/{schedule_id}")
def delete_schedule(schedule_id: int):
    with Session(engine) as session:
        schedule = session.get(Schedule, schedule_id)
        if not schedule:
            raise HTTPException(status_code=404, detail="Schedule not found")
        session.delete(schedule)
        session.commit()
        return {"message": "Schedule deleted"}

# CRUD операции для ScheduleSubject
@app.post("/schedule_subjects/", response_model=ScheduleSubject)
def create_schedule_subject(schedule_subject: ScheduleSubject):
    with Session(engine) as session:
        session.add(schedule_subject)
        session.commit()
        session.refresh(schedule_subject)
        return schedule_subject


@app.get("/schedule_subjects/", response_model=List[ScheduleSubject]) # type: ignore
def read_schedule_subjects():
    with Session(engine) as session:
        schedule_subjects = session.exec(select(ScheduleSubject)).all()
        return schedule_subjects


@app.get("/schedule_subjects/{schedule_subject_id}", response_model=ScheduleSubject)
def read_schedule_subject(schedule_subject_id: int):
    with Session(engine) as session:
        schedule_subject = session.get(ScheduleSubject, schedule_subject_id)
        if not schedule_subject:
            raise HTTPException(status_code=404, detail="ScheduleSubject not found")
        return schedule_subject


@app.put("/schedule_subjects/{schedule_subject_id}", response_model=ScheduleSubject)
def update_schedule_subject(schedule_subject_id: int, schedule_subject: ScheduleSubject):
    with Session(engine) as session:
        db_schedule_subject = session.get(ScheduleSubject, schedule_subject_id)
        if not db_schedule_subject:
            raise HTTPException(status_code=404, detail="ScheduleSubject not found")
        schedule_subject_data = schedule_subject.model_dump(exclude_unset=True)
        for key, value in schedule_subject_data.items():
            setattr(db_schedule_subject, key, value)
        session.add(db_schedule_subject)
        session.commit()
        session.refresh(db_schedule_subject)
        return db_schedule_subject


@app.delete("/schedule_subjects/{schedule_subject_id}")
def delete_schedule_subject(schedule_subject_id: int):
    with Session(engine) as session:
        schedule_subject = session.get(ScheduleSubject, schedule_subject_id)
        if not schedule_subject:
            raise HTTPException(status_code=404, detail="ScheduleSubject not found")
        session.delete(schedule_subject)
        session.commit()
        return {"message": "ScheduleSubject deleted"}

# class User(SQLModel, table=True):
#     __tablename__ = 'user'  # type: ignore

#     id: int | None = Field(default=None, primary_key=True, unique=True)
#     surname: str = Field(max_length=45)
#     name: str = Field(max_length=45)
#     paternity: str | None = Field(max_length=45)
#     gender: str | None = Field(max_length=45)
#     birthdate: datetime | None = Field(default=None)
#     login: str = Field(max_length=25, unique=True)
#     password: str = Field(max_length=25)
#     role_id: int = Field(foreign_key='role.id')


# class Role(SQLModel, table=True):
#     __tablename__ = 'role'  # type: ignore

#     id: int | None = Field(default=None, primary_key=True, unique=True)
#     name: str = Field(max_length=25)


# class Group(SQLModel, table=True):
#     __tablename__ = 'group'  # type: ignore

#     id: int | None = Field(default=None, primary_key=True, unique=True)
#     name: str = Field(max_length=25)


# class UserGroup(SQLModel, table=True):
#     __tablename__ = 'user_group'  # type: ignore

#     id: int | None = Field(default=None, primary_key=True, unique=True)
#     user_id: int = Field(foreign_key='user.id')
#     group_id: int = Field(foreign_key='group.id')


# class Cabinet(SQLModel, table=True):
#     __tablename__ = 'cabinet'  # type: ignore

#     id: int | None = Field(default=None, primary_key=True, unique=True)
#     description: str = Field(max_length=45)


# class Subject(SQLModel, table=True):
#     __tablename__ = 'subject'  # type: ignore

#     id: int | None = Field(default=None, primary_key=True, unique=True)
#     name: str = Field(max_length=50)
#     description: str = Field(max_length=50)
#     type: str = Field(max_length=50)


# class Schedule(SQLModel, table=True):
#     __tablename__ = 'schedule'  # type: ignore

#     id: int | None = Field(default=None, primary_key=True, unique=True)
#     dateandtime: datetime = Field(default_factory=datetime.now)
#     teacher_id: int = Field(foreign_key='user.id')


# class ScheduleSubject(SQLModel, table=True):
#     __tablename__ = 'schedule_subject'  # type: ignore

#     id: int | None = Field(default=None, primary_key=True, unique=True)
#     schedule_id: int = Field(foreign_key='schedule.id')
#     subject_id: int = Field(foreign_key='subject.id')


# class ScheduleCabinet(SQLModel, table=True):
#     __tablename__ = 'schedule_cabinet'  # type: ignore

#     id: int | None = Field(default=None, primary_key=True, unique=True)
#     schedule_id: int = Field(foreign_key='schedule.id')
#     cabinet_id: int = Field(foreign_key='cabinet.id')