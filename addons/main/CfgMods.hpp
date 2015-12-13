class CfgMods {
    class Mod_Base;
    class PREFIX: Mod_Base {
        author = CSTRING(common,Author);
        dir = "@theseus_services";
        name = CSTRING(Name);
        picture = QPATHTOF(UI\logo_tac_ca.paa);
        logo = QPATHTOF(UI\logo_tac_ca.paa);
        logoOver = QPATHTOF(UI\logo_tac_ca.paa);
        logoSmall = QPATHTOF(UI\logo_tac_ca.paa);
        hidePicture = 0;
        hideName = 0;
        actionName = "Website";
        action = "https://github.com/Theseus-Aegis/TheseusServices";
        description = "Issue Tracker: https://github.com/Theseus-Aegis/TheseusServices/issues";
    };
};