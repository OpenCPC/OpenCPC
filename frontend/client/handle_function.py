from .handlers.admin import *
from .handlers.competition import *
from .handlers.general import *
from .handlers.login import *
from .handlers.main_menu import *


async def handle_function(func, params, uobj):
    """Handles (dispatches) a new message to the appropriate handler.

    Args:
        func: The function, as a string, of the message
        params: The parameter list
        uobj: The client's UserObject
    """
    if func == "login":
        await login(uobj, params)
    elif func == "reloadLogin":
        await reloadLogin(params, uobj)
    elif func == "signup":
        await signup(params, uobj)
    elif func == "getMainMenuList":
        await getMainMenuList(params, uobj)
    elif func == "getCompetitionInfo":
        await getCompetitionInfo(params, uobj)
    elif func == "getProblemList":
        await getProblemList(params, uobj)
    elif func == "adminProblems":
        await adminProblems(params, uobj)
    elif func == "adminCompetitors":
        await adminCompetitors(params, uobj)
    elif func == "getSubmissions":
        await getSubmissions(params, uobj)
    elif func == "openProblem":
        await openProblem(params, uobj)
    elif func == "submitProblem":
        await submitProblem(params, uobj)
    elif func == "getMainMenuSPS":
        await getMainMenuSPS(params, uobj)
    elif func == "getPopUp":
        await getPopUp(params, uobj)
    elif func == "adminGetPopUp":
        await getPopUp(params, uobj)
    elif func == "createComp":
        await createComp(params, uobj)
    elif func == "editComp":
        await editComp(params, uobj)
    elif func == "loadAdmin":
        await loadAdmin(params, uobj)
    elif func == "getScoreboard":
        await getScoreboard(params, uobj)
    elif func == "getAllSubmissions":
        await getAllSubmissions(params, uobj)
    elif func == "getAdminProblem":
        await getAdminProblem(params, uobj)
    elif func == "addCompetitor":
        await addCompetitor(params, uobj)
    elif func == "editCompetitor":
        await editCompetitor(params, uobj)
    elif func == "adminSubmissions":
        await adminSubmissions(params, uobj)
    elif func == "adminScoreboard":
        await getScoreboard(params, uobj)
    elif func == "forgotPassword":
        await forgotPassword(params, uobj)
    elif func == "resetPassword":
        await resetPassword(params, uobj)
    elif func == "adminGetCase":
        await adminGetCase(params, uobj)
    elif func == "adminSaveQuestion":
        await adminSaveQuestion(params, uobj)
    elif func == "adminSaveCase":
        await adminSaveCase(params, uobj)
    elif func == "adminRemoveCase":
        await adminRemoveCase(params, uobj)
    elif func == "adminRemoveProblem":
        await adminRemoveProblem(params, uobj)
    elif func == "adminAddCase":
        await adminAddCase(params, uobj)
    elif func == "adminAddProblem":
        await adminAddProblem(params, uobj)
    elif func == "adminAddImage":
        await adminAddImage(params, uobj)
    elif func == "adminRemoveImage":
        await adminRemoveImage(params, uobj)
    elif func == "adminLevels":
        await adminLevels(params, uobj)
    elif func == "adminDeleteLevel":
        await adminDeleteLevel(params, uobj)
    elif func == "adminSaveLevel":
        await adminSaveLevel(params, uobj)
    elif func == "adminAddLevel":
        await adminAddLevel(params, uobj)
    elif func == "adminRegradeProblemSubmissions":
        await adminRegradeProblemSubmissions(params, uobj)
    elif func == "adminControlPanel":
        await adminControlPanel(params, uobj)
    elif func == "removeCompetitor":
        await removeCompetitor(params, uobj)
    elif func == "moveProblem":
        await moveProblem(params, uobj)
    elif func == "adminSetCompStatus":
        await adminSetCompStatus(params, uobj)
    elif func == "adminSetAutomaticCompetitionStatus":
        await adminSetAutomaticCompetitionStatus(params, uobj)
    elif func == "adminSetScoreboard":
        await adminSetScoreboard(params, uobj)
    elif func == "customrun":
        await adminCustomRun(params, uobj)
    elif func == "adminCompetitorInfo":
        await adminCompetitorInfo(params, uobj)
    elif func == "returnFromFieldSub":
        pass
    elif func == "adminGroups":
        await adminGroups(params, uobj)
    elif func == "adminDeleteGroup":
        await adminDeleteGroup(params, uobj)
    elif func == "adminSaveGroup":
        await adminSaveGroup(params, uobj)
    elif func == "adminAddGroup":
        await adminAddGroup(params, uobj)
    elif func == "joinComp":
        await joinComp(params, uobj)
    else:
        print("Unknown message from client:", params)
