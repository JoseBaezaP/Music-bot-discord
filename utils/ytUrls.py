
import re

from urllib import parse, request

def createUrl(search):
  query_string = parse.urlencode({"search_query": search})
  html_content = request.urlopen('https://www.youtube.com/results?' + query_string)
  search_result = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())

  video_url = "https://www.youtube.com/watch?v=" + search_result[0]
  return video_url
