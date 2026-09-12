SCORES={"Official":100,"Verified source":90,"Reliable citizen":80,"Normal citizen":60,"New/untrusted":40}
def score(source): return SCORES.get(source,60)
