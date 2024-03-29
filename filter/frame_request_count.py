# Idea taken from Setsugen no ao but I can't find link to the original snippet
import vapoursynth as vs
from vapoursynth import core

def frame_request_count(clip: vs.VideoNode) -> vs.VideoNode:
    requests = dict()
    def _check(n:int, f: vs.VideoFrame):
        fout = f.copy()
        if n in requests:
            requests[n] += 1
            core.log_message(vs.MESSAGE_TYPE_DEBUG,
                             f'Frame {n} has been requested for {requests[n]} times.')
        else:
            requests[n] = 1
        return fout
    return core.std.ModifyFrame(clip, clip, _check)

if __name__ == '__main__':
    clip = core.std.BlankClip()
    clip = frame_request_count(clip)
    clip.set_output()
