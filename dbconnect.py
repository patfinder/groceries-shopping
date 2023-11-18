from typing import List
from typing import Optional
from sqlalchemy import create_engine, select
from sqlalchemy import ForeignKey, String, Double, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import Session

class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[str] = mapped_column(String(200), primary_key=True)
    retailer: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    categories: Mapped[str] = mapped_column(String(100))
    image: Mapped[str] = mapped_column(String(200))
    url: Mapped[str] = mapped_column(String(200))
    price: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f'Product(id={self.id!r}, name={self.name!r})'


class Manufacturer(Base):
    __tablename__ = 'manufacturer'

    id: Mapped[int] = mapped_column(primary_key=True)
    # email_address: Mapped[str]
    # user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    #
    # user: Mapped["User"] = relationship(back_populates="addresses")
    #
    # def __repr__(self) -> str:
    #     return f'Address(id={self.id!r}, email_address={self.email_address!r})'


def add_products(products):
    engine = create_engine(f'mysql+pymysql://groceries:groceries_pass@localhost/groceries_db', echo=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add_all(products)
        session.commit()


def select1():
    # session = Session(engine)
    # stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))
    # for user in session.scalars(stmt):
    #     print(user)
    #
    # # Select with join
    # stmt = (
    #     select(Address)
    #     .join(Address.user)
    #     .where(User.name == "sandy")
    #     .where(Address.email_address == "sandy@sqlalchemy.org")
    # )
    # sandy_address = session.scalars(stmt).one()
    pass
