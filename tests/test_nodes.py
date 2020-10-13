import json
from random import randrange

import jsonlines
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# from tinydb import TinyDB

BENCH_RECORDS = 1e5
BENCH_ROUNDS_WRITE = 5
BENCH_ROUNDS_QUERY = 1000


def write_json(archive, node_generator, records):
    data = {}
    for node in node_generator(int(records)):
        data[str(node.uuid)] = {"attr1": "string"}
    with archive.open("w") as handle:
        json.dump(data, handle)


def query_json(archive, uuid):
    with archive.open("r") as handle:
        data = json.load(handle)
    return data.get(uuid, None)


def write_jsonlines(archive, node_generator, records):
    with jsonlines.open(str(archive), mode="w") as writer:
        for node in node_generator(int(records)):
            data = {"uuid": str(node.uuid), "attr1": "string"}
            writer.write(data)


def query_jsonlines(archive, uuid):
    with jsonlines.open(str(archive), mode="r") as reader:
        for obj in reader.iter(type=dict, skip_invalid=True):
            if obj.get("uuid", None) == uuid:
                return uuid
    return None


Base = declarative_base()


class Node(Base):
    """Node."""

    __tablename__ = "db_node"

    pk = Column(Integer, primary_key=True)
    uuid = Column(String, nullable=False, unique=True, index=True)
    attr = Column(String)


def get_session(path, create=True) -> Session:
    """Return a new session to connect to the pack-index SQLite DB.

    :param create: if True, creates the sqlite file and schema.
    """
    engine = create_engine("sqlite:///{}".format(path))

    if create:
        # Create all tables in the engine.
        Base.metadata.create_all(engine)

    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    return session


def write_sqlite(archive, node_generator, records):
    session = get_session(str(archive))
    try:
        for node in node_generator(int(records)):
            session.add(Node(uuid=str(node.uuid), attr="string"))
        session.commit()
    finally:
        session.close()


def query_sqlite(archive, uuid):
    session = get_session(str(archive))
    try:
        query = session.query(Node)
        node = query.filter(Node.uuid == uuid).one_or_none()
    finally:
        session.close()
    return node


# too slow!
# def write_tinydb(archive, node_generator, records):
#     with TinyDB(str(archive)) as db:
#         for node in node_generator(int(records)):
#             data = {"uuid": str(node.uuid), "attr1": "string"}
#             db.insert(data)


# def test_write_tinydb(benchmark, tmp_path, node_generator):
#     archive = tmp_path / "archive.json"

#     def _setup():
#         if archive.exists():
#             archive.unlink()

#     benchmark.pedantic(
#         write_tinydb,
#         args=(archive, node_generator, BENCH_RECORDS),
#         setup=_setup,
#         rounds=BENCH_ROUNDS_WRITE,
#     )


def test_write_json(benchmark, tmp_path, node_generator):
    archive = tmp_path / "archive.json"

    def _setup():
        if archive.exists():
            archive.unlink()

    benchmark.pedantic(
        write_json,
        args=(archive, node_generator, BENCH_RECORDS),
        setup=_setup,
        rounds=BENCH_ROUNDS_WRITE,
    )


def test_write_jsonlines(benchmark, tmp_path, node_generator):
    archive = tmp_path / "archive.jsonl"

    def _setup():
        if archive.exists():
            archive.unlink()

    benchmark.pedantic(
        write_jsonlines,
        args=(archive, node_generator, BENCH_RECORDS),
        setup=_setup,
        rounds=BENCH_ROUNDS_WRITE,
    )


def test_write_sqlite(benchmark, tmp_path, node_generator):
    archive = tmp_path / "archive.sqlite"

    def _setup():
        if archive.exists():
            archive.unlink()

    benchmark.pedantic(
        write_sqlite,
        args=(archive, node_generator, BENCH_RECORDS),
        setup=_setup,
        rounds=BENCH_ROUNDS_WRITE,
    )


def test_query_json(benchmark, tmp_path, node_generator):
    archive = tmp_path / "archive.json"
    write_json(archive, node_generator, BENCH_RECORDS)

    def _setup():
        number = randrange(BENCH_RECORDS)
        uuid = f"{hex(int(number)):0>36}"
        return (archive, uuid), {}

    output = benchmark.pedantic(
        query_json,
        setup=_setup,
        rounds=BENCH_ROUNDS_QUERY,
    )
    assert output is not None


def test_query_jsonlines(benchmark, tmp_path, node_generator):
    archive = tmp_path / "archive.json"
    write_jsonlines(archive, node_generator, BENCH_RECORDS)

    def _setup():
        number = randrange(BENCH_RECORDS)
        uuid = f"{hex(int(number)):0>36}"
        return (archive, uuid), {}

    output = benchmark.pedantic(
        query_jsonlines,
        setup=_setup,
        rounds=BENCH_ROUNDS_QUERY,
    )
    assert output is not None


def test_query_sqlite(benchmark, tmp_path, node_generator):
    archive = tmp_path / "archive.sqlite"
    write_sqlite(archive, node_generator, BENCH_RECORDS)

    def _setup():
        number = randrange(BENCH_RECORDS)
        uuid = f"{hex(int(number)):0>36}"
        return (archive, uuid), {}

    output = benchmark.pedantic(
        query_sqlite,
        setup=_setup,
        rounds=BENCH_ROUNDS_QUERY,
    )
    assert output is not None
