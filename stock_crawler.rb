stocks = ['AAPL', 'TSLA', 'TWTR', 'GOOG']
to_month = 2
to_year = 2015
from_year = 2015
from_month = 2
from_day = 01
to_day = 31

stocks.each do |stock|
  url = "http://ichart.finance.yahoo.com/table.csv?s=#{stock}&d=#{to_month}&e=#{to_day}&f=#{to_year}&g=d&a=#{from_month}&b=#{from_day}&c=#{from_year}&ignore=.csv"
  `wget #{url}`
  `mv table* data/stock_#{stock}.csv`
end
