from src.mhd_twoflow_nmsi import twoflow_step

def test_step():
    u1,u2 = twoflow_step(1,0.5,0.01,(0.1,0.05,0.01))
    assert isinstance(u1,float)
    assert isinstance(u2,float)
