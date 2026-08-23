#include "ArchicadDevPrecompiledHeader.hpp"

#include "ResourceIds.hpp"
#include "RS.hpp"

namespace {

constexpr GSResID AddOnInfoID = ID_ADDON_INFO;
constexpr Int32 AddOnNameID = 1;
constexpr Int32 AddOnDescriptionID = 2;
constexpr short AddOnMenuID = ID_ADDON_MENU;

GSErrCode MenuCommandHandler(const API_MenuParams* menuParams)
{
    if (menuParams->menuItemRef.menuResID == AddOnMenuID) {
        ACAPI_WriteReport("ArchicadDevAddOn command invoked.", true);
    }
    return NoError;
}

} // namespace

API_AddonType CheckEnvironment(API_EnvirParams* envir)
{
    RSGetIndString(&envir->addOnInfo.name, AddOnInfoID, AddOnNameID, ACAPI_GetOwnResModule());
    RSGetIndString(&envir->addOnInfo.description, AddOnInfoID, AddOnDescriptionID, ACAPI_GetOwnResModule());
    return APIAddon_Normal;
}

GSErrCode RegisterInterface()
{
#ifdef ServerMainVers_2700
    return ACAPI_MenuItem_RegisterMenu(AddOnMenuID, 0, MenuCode_Tools, MenuFlag_Default);
#else
    return ACAPI_Register_Menu(AddOnMenuID, 0, MenuCode_Tools, MenuFlag_Default);
#endif
}

GSErrCode Initialize()
{
#ifdef ServerMainVers_2700
    return ACAPI_MenuItem_InstallMenuHandler(AddOnMenuID, MenuCommandHandler);
#else
    return ACAPI_Install_MenuHandler(AddOnMenuID, MenuCommandHandler);
#endif
}

GSErrCode FreeData()
{
    return NoError;
}
