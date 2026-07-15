from sqlalchemy import create_engine, Integer, String, Column, Float, ForeignKey, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base

# DATABASE_URL = "mysql+pysql://root:123456@localhost:3306"

# engine = create_engine(DATABASE_URL)
# Sessionmaker = sessionmaker(bind=engine)

package_truck = Table(
    "package_truck",
    Base.metadata,
    Column("package_id", ForeignKey("package.id"), primary_key=True),
    Column("truck_id", ForeignKey("truck.id"), primary_key=True)

)

class Warehouse(Base):
    __tablename__ = "warehouse"
    id = Column(Integer, primary_key=True)
    warehouse_name = Column(String(180), nullable=False)
    location = Column(String(255), nullable=False)
    
    
    packages = relationship("Package", back_populates= "warehouse")


class Package(Base):
    __tablename__ = "packages"
    id = Column(Integer, primary_key= True)
    package_code = Column(String(10), unique= True, nullable=True)
    weight = Column(Float, nullable=False)
    
    warehouse_id = Column(Integer, ForeignKey("warehouse.id"))
    
    warehouse = relationship("Warehouse", back_populates="packages")
    
    waybill = relationship("Waybill", back_populates="package", uselist=False , cascade="all, delete-orphan")
    truck = relationship("Truck", secondary=package_truck ,back_populates="packages")
    
    
class Waybill(Base):
    __tablename__ = "waybills"
    id = Column(Integer, primary_key=True)
    tracking_number = Column(String(100), nullable=False)
    shipping_status = Column(String(100), nullable=False)
    
    package_id = Column(Integer, ForeignKey("packages.id"), nullable=False, unique=True)
    
    package = relationship("Package", back_populates= "Waybill", uselist= False, cascade="all, delete-orphan")
    
    
class Truck(Base):
    __tablename__ = "trucks"
    id = Column(Integer, primary_key=True)
    license_plate = Column(String(10), nullable=False)
    
    packages = relationship("Package", secondary=package_truck, back_populates="trucks")
    
    
    