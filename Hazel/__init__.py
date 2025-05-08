from Essentials import *
from MultiSessionManagement.decorators import *

x = CreateClients(Init())
app, bot, DATABASE = x.app, x.bot, x.DATABASE