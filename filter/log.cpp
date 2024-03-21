#include <vapoursynth/VapourSynth4.h>

const VSFrame * VS_CC filterGetFrame(int n, int activationReason, void *instanceData, void **frameData, VSFrameContext *frameCtx, VSCore *core, const VSAPI *vsapi)
{
    VSNode *node = reinterpret_cast<VSNode *>(instanceData);
    if (activationReason == arInitial)
    {
        vsapi->logMessage(mtInformation, "info: request frame", core);
        vsapi->requestFrameFilter(n, node, frameCtx);
    }
    else if (activationReason == arAllFramesReady)
    {
        const VSFrame *frame = vsapi->getFrameFilter(n, node, frameCtx);
        vsapi->logMessage(mtInformation, "info: getFrame", core);
        return frame;
    }
    return nullptr;
}

void VS_CC filterFree(void *instanceData, VSCore *core, const VSAPI *vsapi)
{
    vsapi->logMessage(mtInformation, "info: free", core);
    vsapi->freeNode(reinterpret_cast<VSNode *>(instanceData));
}

void VS_CC filterCreate(const VSMap *in, VSMap *out, void *userData, VSCore *core, const VSAPI *vsapi)
{
    VSNode *node = vsapi->mapGetNode(in, "clip", 0, nullptr);
    VSFilterDependency deps[] = {{node, rpStrictSpatial}};
    vsapi->logMessage(mtInformation, "info: creating filter", core);
    vsapi->createVideoFilter(out, "Log", vsapi->getVideoInfo(node), filterGetFrame, filterFree, fmParallel, deps, 1, node, core);
    vsapi->logMessage(mtInformation, "info: filter created", core);
}

VS_EXTERNAL_API(void) VapourSynthPluginInit2(VSPlugin *plugin, const VSPLUGINAPI *vspapi) {
    vspapi->configPlugin("test.log.filter", "test_log_filter", "Log", VS_MAKE_VERSION(1, 0), VAPOURSYNTH_API_VERSION, 0, plugin);
    vspapi->registerFunction("Filter", "clip:vnode;", "clip:vnode;", filterCreate, NULL, plugin);
}
