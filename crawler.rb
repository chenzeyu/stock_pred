require 'rest_client'
require 'json'
URL = "http://otter.topsy.com/search.json"

lang = 'en'
perpage = 100
start_time = Time.new(2015,03,1, "+08:00").to_i
end_time = Time.new(2015,03,15, "+08:00").to_i
timestamp = Time.now.to_i
apikey = '09C43A9B270A470B8EB8F2946A9369F3'
type = 'tweet'
query = ['$aapl','$twtr', '$goog', '$tsla']
query.each do |q|
  offset = 0
  jsons = []
  loop do
    RestClient.get(URL, {params:
                         {
      allow_lang:lang,
      offset:offset,
      type: type,
      perpage: perpage,
      mintime:start_time,
      maxtime:end_time,
      call_timestamp: timestamp,
      q: q,
      apikey: apikey}
    }) {|response, request, result|
      json = JSON.parse(response)
      jsons << json['response']['list']
      offset += json['response']['last_offset'].to_i
      puts "Current Offset: #{offset}"
    }
    break if offset >= 50000
  end
  merged = []
  jsons.each {|a| merged += a}
  File.open("data/#{q[1..-1]}.json",'a') {|f| f.write merged.to_json}
end

