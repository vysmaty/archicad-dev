#include "ArchicadDevPrecompiledHeader.hpp"

#include "compat/ArchicadCompatibility.hpp"

namespace ACCompat {

GSErrCode RegisterMenu(short menuResourceId)
{
    return ACAPI_MenuItem_RegisterMenu(
        menuResourceId, 0, MenuCode_Tools, MenuFlag_Default
    );
}

} // namespace ACCompat
