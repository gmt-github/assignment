import unittest
from assignment import  count_per_day_data, count_per_day_user_agent_data, count_os_per_day_verb_data


class AssignmentTest(unittest.TestCase):
    sample_data = """127.0.0.1 - - [01/Dec/2011:00:05:24 -0500] "GET /post/twenty-five-songs/ HTTP/1.0" 200 35309 "http://aviflax.com/post/twenty-five-songs/" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Deepnet Explorer 1.5.0; .NET CLR 1.0.3705)"
127.0.0.1 - - [01/Dec/2011:00:05:31 -0500] "POST /wp-comments-post.php HTTP/1.0" 302 441 "http://aviflax.com/post/twenty-five-songs/" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Deepnet Explorer 1.5.0; .NET CLR 1.0.3705)"
127.0.0.1 - - [01/Dec/2011:00:05:35 -0500] "GET /post/twenty-five-songs/ HTTP/1.0" 200 35426 "http://aviflax.com/post/twenty-five-songs/" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Deepnet Explorer 1.5.0; .NET CLR 1.0.3705)"
"""

    def test_count_per_day_data(self):
        date_wise_count = count_per_day_data(self.sample_data)
        for k, v in date_wise_count.items():
            assert str(k) == "01/Dec/2011"
            assert str(v) == "3"

    def test_count_per_day_user_agent_data(self):
        data_user_agent_wise = count_per_day_user_agent_data(self.sample_data)
        for k, v in data_user_agent_wise.items():
            assert str(k[0]) == "01/Dec/2011"
            assert str(k[-1]) == "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Deepnet Explorer 1.5.0; .NET CLR 1.0.3705)"
            assert str(v) == "3"

    def test_count_os_per_day_verb_data(self):
        data_verb_wise = count_os_per_day_verb_data(self.sample_data)
        for k, v in data_verb_wise.items():
            assert str(k) == "01/Dec/2011"
        assert data_verb_wise['01/Dec/2011']['Windows']['GET'] == {2}
        assert data_verb_wise['01/Dec/2011']['Windows']['POST'] == {1}
