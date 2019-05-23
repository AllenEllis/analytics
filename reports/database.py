from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sqa
import time

Base = declarative_base()


class Connect():
    """A class for accessing a temporary SQLite database. This
    function works as a context manager and should be used as follows:

    with Connect() as db:
        (Perform operation here)
    """

    def __init__(self, engine=None):
        """Initialize the database."""
        if engine is None:
            engine = 'sqlite:///temp.db'
        self.engine = sqa.create_engine(engine)
        self.session = sqa.orm.sessionmaker(bind=self.engine)
        self.meta = Base.metadata
        self.meta.create_all(self.engine)

    def __enter__(self):
        """This function is automatically called whenever the class
        is used together with a 'with' statement.
        """
        self.cursor = self.session()

        return self

    def __exit__(self, type, value, tb):
        """Upon exiting the 'with' statement, __exit__ is called."""
        self.cursor.commit()
        self.cursor.close()


class CLoverRaw():
    __tablename__ = 'cloverraw'


class Orders(Base):
    __tablename__ = 'orders'
    id = sqa.Column(sqa.String(13), primary_key=True)

    clientCreatedTime = sqa.Column(sqa.BigInteger)  # 1508272429000
    createdTime = sqa.Column(sqa.BigInteger)  # 1508272430000,
    currency = sqa.Column(sqa.String(16))  # USD,
    customerID = sqa.Column(sqa.String(13))  # "RW2P3N7BPYVGM"
    deviceID = sqa.Column(sqa.String(64))  # b392cb47-93e9-4aff-8357-7a6407c08a58
    employee = sqa.Column(sqa.String(13))  # SC9VSVBV81PMP
    groupLineItems = sqa.Column(sqa.Boolean)  # true
    href = sqa.Column(sqa.String(128))  # www.clover.com/v3/merchants/DS3DVBKPGW666/orders/003APMKTYAV4E
    isVat = sqa.Column(sqa.Boolean)  # false
    manualTransaction = sqa.Column(sqa.Boolean)  # false
    modifiedTime = sqa.Column(sqa.BigInteger)  # 1508303600000
    note = sqa.Column(sqa.String(3000))
    orderType = sqa.Column(sqa.String(128))
    payType = sqa.Column(sqa.String(128))  # FULL
    state = sqa.Column(sqa.String(128))  # locked
    taxRemoved = sqa.Column(sqa.Boolean)  # false
    testMode = sqa.Column(sqa.Boolean)  # false
    title = sqa.Column(sqa.String(128))  # TO GO 1
    total = sqa.Column(sqa.Integer)  # 3012

    def __init__(self, order):
        self.id = order.get('id')
        self.clientCreatedTime = order.get('clientCreatedTime')
        self.createdTime = order.get('createdTime')
        self.currency = order.get('currency')
        customer = order.get('customers')
        if customer:
            self.customerID = customer['elements'][0]['id']
        device = order.get('device')
        if device:
            self.deviceID = device.get('id')
        employee = order.get('employee')
        if employee:
            self.employee = employee.get('id')
        self.groupLineItems = order.get('groupLineItems')
        self.href = order.get('href')
        self.isVat = order.get('isVat')
        self.manualTransaction = order.get('manualTransaction')
        self.modifiedTime = order.get('modifiedTime')
        self.note = order.get('note')
        orderType = order.get('orderType')
        if orderType:
            self.orderType = orderType.get('id')
        self.payType = order.get('payType')
        self.state = order.get('state')
        self.taxRemoved = order.get('taxRemoved')
        self.testMode = order.get('testMode')
        self.title = order.get('title')
        self.total = order.get('total')

        # CloverRaw(order)


class LineItems(Base):
    __tablename__ = 'lineitems'
    id = sqa.Column(sqa.String(13), primary_key=True)

    alternateName = sqa.Column(sqa.String(128))
    binName = sqa.Column(sqa.String(128))
    createdTime = sqa.Column(sqa.BigInteger)  # 1520375184000
    exchanged = sqa.Column(sqa.Boolean)  # false
    isRevenue = sqa.Column(sqa.Boolean)  # true
    itemID = sqa.Column(sqa.String(13))  # RDPWQQ37TK9SE
    itemCode = sqa.Column(sqa.String(128))
    name = sqa.Column(sqa.String(3000))  # NITRO Espresso Roast - Coffee 12 OZ
    orderClientCreatedTime = sqa.Column(sqa.BigInteger)  # 1520375184000
    price = sqa.Column(sqa.Integer)  # 450
    printed = sqa.Column(sqa.Boolean)  # true
    refunded = sqa.Column(sqa.String(13))  # 775Q9VWZH61MT

    orderID = sqa.Column(sqa.String(13), sqa.ForeignKey('orders.id'))  # PC6049E1GFK0W
    order = sqa.orm.relationship('Orders', uselist=False)

    def __init__(self, lineitem):
        self.id = lineitem.get('id')
        self.alternateName = lineitem.get('alternateName')
        self.binName = lineitem.get('binName')
        self.createdTime = lineitem.get('createdTime')
        self.exchanged = lineitem.get('exchanged')
        self.isRevenue = lineitem.get('isRevenue')
        item = lineitem.get('item')
        if item:
            self.itemID = item.get('id')
        self.itemCode = lineitem.get('itemCode')
        self.name = lineitem.get('name')
        self.orderClientCreatedTime = lineitem.get('orderClientCreatedTime')
        order = lineitem.get('orderRef')
        if order:
            self.orderID = order.get('id')
        self.price = lineitem.get('price')
        self.printed = lineitem.get('printed')
        self.refunded = lineitem.get('refunded')


class Events(Base):
    __tablename__ = 'events'
    id = sqa.Column(sqa.Integer, primary_key=True)

    scheduled = sqa.Column(sqa.Boolean)
    tag = sqa.Column(sqa.String)
    title = sqa.Column(sqa.String)
    startTime = sqa.Column(sqa.Integer)
    endTime = sqa.Column(sqa.Integer)
    summary = sqa.Column(sqa.String)
    image = sqa.Column(sqa.String)

    def __init__(self, googleRow):
        length = len(googleRow)
        self.id = googleRow[0]

        scheduled = googleRow[1]
        if scheduled == 'FALSE':
            self.scheduled = False
        else:
            self.scheduled = True

        self.tag = googleRow[2]
        self.title = googleRow[3]

        date = googleRow[4]

        if length > 5:
            start = date + ' ' + googleRow[5]
            sEpoch = int(time.mktime(time.strptime(start, '%Y-%m-%d %H:%M')))
        else:
            sEpoch = int(time.mktime(time.strptime(date, '%Y-%m-%d')))
        self.startTime = sEpoch

        if length > 6:
            end = date + ' ' + googleRow[6]
            eEpoch = int(time.mktime(time.strptime(end, '%Y-%m-%d %H:%M')))
        else:
            eEpoch = int(time.mktime(time.strptime(date, '%Y-%m-%d')))
        self.endTime = eEpoch

        if length > 7:
            self.summary = googleRow[7]

        if length > 8:
            self.image = googleRow[8]