from pagerank import transition_model, sample_pagerank, iterate_pagerank


test_sample = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
page = "1.html"
damp = 0.85
s = 10000




#sample_pagerank(test_sample, damp, s)

iterate_pagerank(test_sample, damp)




