#pragma once

#include "ACAPinc.h"

namespace ACCompat {

GSErrCode RegisterMenu(short menuResourceId);

template<typename MenuHandler>
GSErrCode InstallMenuHandler(short menuResourceId, MenuHandler handler)
{
    return ACAPI_MenuItem_InstallMenuHandler(menuResourceId, handler);
}

} // namespace ACCompat
