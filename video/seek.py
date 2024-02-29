import hashlib
import random
import vapoursynth as vs
from vapoursynth import core

__all__ = ['compare_with_bs']

def compare_with_bs(fn, filter, frame_range: list | None = None, max_tol: int = 2):
    bs_clip = core.bs.VideoSource(fn, seekpreroll=0)
    clip = filter(fn)

    if len(bs_clip) != len(clip):
        print(r'Warning: clip length mismatch.')

    if frame_range is None:
        frame_range = list(range(len(bs_clip)))

    def hash_frame(frame):
        sha256 = hashlib.sha256()
        for plane in range(frame.format.num_planes):
            sha256.update(frame[plane].tobytes())
        return sha256.hexdigest()

    ref = dict()
    for n in frame_range:
        ref[n] = hash_frame(bs_clip.get_frame(n))
        print(f'...hashing frame {n:7} with BS...', end='\r')
    print('\nDone.')

    random.shuffle(frame_range)
    error_tol = max(0, max_tol)
    for i in range(len(frame_range)):
        n = frame_range[i]
        try:
            result = hash_frame(clip.get_frame(n))
            if result != ref[n]:
                print(f'\nMismatch on frame {n}.')
                error_tol -= 1
                if error_tol < 0:
                    print('Abort.')
                    return
        except vs.Error as e:
            print(f'Requesting frame {n} broke source filter.')
            raise e
        print(f'...hashing frame {n:7} with provided filter... {(i + 1):7} / {len(frame_range)}', end='\r')
    print('\nPassed.')
