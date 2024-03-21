import vapoursynth as vs
core = vs.core

clip = core.std.BlankClip(length=1)
clip = core.test_log_filter.Filter(clip)
clip.set_output()
