"""
    @author: ArcREST Team
    @contact: www.github.com/Esri/ArcREST
    @company: Esri
    @version: 1.0.0
    @description: deletes a group on the AGOL site.
    @requirements: Python 2.7.x, ArcGIS 10.2.2, ArcREST 2.0
    @copyright: Esri, 2015
"""
import os
from arcpy import env
from arcpy import mapping
from arcpy import da
import arcpy
import configparser
import arcrest
#--------------------------------------------------------------------------
class FunctionError(Exception):
    """ raised when a function fails to run """
    pass
#--------------------------------------------------------------------------
def trace():
    """
        trace finds the line, the filename
        and error message and returns it
        to the user
    """
    import traceback
    import sys
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    # script name + line number
    line = tbinfo.split(", ")[1]
    # Get Python syntax error
    #
    synerror = traceback.format_exc().splitlines()[-1]
    return line, __file__, synerror
#--------------------------------------------------------------------------
def main(*argv):
    """ main driver of program """
    try:
        #   Inputs
        #
        adminUsername = argv[0]
        adminPassword = argv[1]
        siteURL = argv[2]
        groupName = argv[3]
        #   Logic
        #
        sh = arcrest.AGOLTokenSecurityHandler(adminUsername, adminPassword)
        admin = arcrest.manageorg.Administration(securityHandler=sh)
        community = admin.community
        g = community.getGroupIDs(groupNames=[groupName])
        if len(g) == 0:
            arcpy.AddWarning("No Group Exists with That Name %s" % groupName)
            arcpy.SetParameterAsText(4, False)
        elif len(g) == 1:
            groups = community.groups
            groups.deleteGroup(groupId=g[0])
            arcpy.AddWarning("%s was erased." % groupName)
            arcpy.SetParameterAsText(4, True)
        else:
            arcpy.AddError("Multiple group names found, please manually delete!")
            arcpy.SetParameterAsText(4, False)
    except arcpy.ExecuteError:
        line, filename, synerror = trace()
        arcpy.AddError("error on line: %s" % line)
        arcpy.AddError("error in file name: %s" % filename)
        arcpy.AddError("with error message: %s" % synerror)
        arcpy.AddError("ArcPy Error Message: %s" % arcpy.GetMessages(2))
    except FunctionError as f_e:
        messages = f_e.args[0]
        arcpy.AddError("error in function: %s" % messages["function"])
        arcpy.AddError("error on line: %s" % messages["line"])
        arcpy.AddError("error in file name: %s" % messages["filename"])
        arcpy.AddError("with error message: %s" % messages["synerror"])
        arcpy.AddError("ArcPy Error Message: %s" % messages["arc"])
    except:
        line, filename, synerror = trace()
        arcpy.AddError("error on line: %s" % line)
        arcpy.AddError("error in file name: %s" % filename)
        arcpy.AddError("with error message: %s" % synerror)
#--------------------------------------------------------------------------
if __name__ == "__main__":
    env.overwriteOutput = True
    argv = tuple(str(arcpy.GetParameterAsText(i))
        for i in range(arcpy.GetArgumentCount()))
    main(*argv)