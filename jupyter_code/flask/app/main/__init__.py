# 寫的比較結構化, 有很多資料夾 + 處理方式
# 需要Blueprint
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views
