import vapoursynth as vs
core = vs.core

def aa_test_clip(size: int = 200):
    SUBTITLE_DEFAULT_STYLE: str = (f"arial,{size},&H00FFFFFF,&H000000FF,&H00000000,&H00000000,"
                                "0,0,0,0,100,100,0,0,1,2,0,7,10,10,10,1")

    clip = core.std.BlankClip(format=vs.YUV444PS, width=size * 5, height=size)
    clip = core.sub.Subtitle(clip, text="1234567890", style=SUBTITLE_DEFAULT_STYLE)
    return clip
