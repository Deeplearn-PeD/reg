from sqlmodel import SQLModel, Field, create_engine, Session, select
import datetime
import loguru

logger = loguru.get_logger()

class Problem(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now, index=True)
    session_id: str = Field() #md5 hash of the session
    question: str = Field()
    context: str = Field()
    code: str = Field()
    explanation: str = Field()


class History:
    def __init__(self, dburl: str = "sqlite://"):
        self.engine = self._setup_db(dburl)

    def _setup_db(self, dburl: str)->object:
        """
        Setup the database
        :param dburl: database url
        :return:
        """
        engine = create_engine(dburl)
        SQLModel.metadata.create_all(engine)
        return engine

    def memorize(self, session_id: int, question: str, code: str, explanation: str, context: str)->Problem:
        """
        Persist a chat in the database
        :param session_id: id of the chat session
        :param question: question asked
        :param code: code snippet to answer the question
        :param explanation: explanation of the code
        :param context: context of the question
        :return: memory object
        """
        with Session(self.engine) as session:
            memory = Problem(session_id=session_id, question=question, code=code, explanation=explanation, context=context)
            session.add(memory)
            session.commit()
            session.refresh(memory)
        return memory

    def recall(self, session_id, since: datetime.datetime = None):
        with Session(self.engine) as session:
            if since:
                stmt = select(Problem).where(Problem.session_id == session_id).where(Problem.timestamp >= since)
            else:
                stmt = select(Problem).where(Problem.session_id == session_id)
            results = session.exec(stmt).fetchall()
        return results