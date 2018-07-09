import sys
import os

def getClientVersionInHeaderFile(marketCode, versionKind, versionHeaderFile):
    MONO_PATH = '/Applications/Unity/Unity.app/Contents/MonoBleedingEdge/bin/mono'
    option = optionparser(marketCode, versionKind, versionHeaderFile)
    makePrintCsScript()
    csCompile(option, versionHeaderFile)
    # mono로 exe 실행
    os.system(MONO_PATH+' getClientVersionInHeaderFile')
    deleteTempFiles()


def deleteTempFiles():
    # 실행 위치에 따라 cs파일이 남아있으면 유니티 빌드에 영향을 줄 수도 있으니 삭제
    os.system("rm printBuild.cs")
    os.system("rm getClientVersionInHeaderFile")

def csCompile(option, versionHeaderFile):
    # mac 한정으로 exe파일 실행시 mono 실행이 필요함
    MONO_PATH   = '/Applications/Unity/Unity.app/Contents/MonoBleedingEdge/bin/mono'
    MCS_PATH    = '/Applications/Unity/Unity.app/Contents/MonoBleedingEdge/lib/mono/4.5/mcs.exe'
    print(MONO_PATH+' '+MCS_PATH+' '+option+' '+versionHeaderFile+' '+"printBuild.cs")
    os.system(MONO_PATH+' '+MCS_PATH+' '+option+' '+versionHeaderFile+' '+"printBuild.cs")


def makePrintCsScript():
    fp= open("printBuild.cs", 'w')
    # build.cs 안의 다른 정보가 필요할 경우 WriteLine을 추가하세요
    print(  "using System;\n" +
            "using System.Collections;\n" +
            "public class printBuild\n" +
            "{\n" +
            "   static void Main(string[] args)\n" +
            "   {\n" +
            "       Console.WriteLine(\"CLIENT_VER=\"+Build.CLIENT_VER);\n" +
            "   }\n" +
            "}\n", file=fp)
    fp.close()


def optionparser(marketCode, versionKind, versionHeaderFile):
    option= '-target:exe -nowarn:0169 -langversion:4 -out:getClientVersionInHeaderFile\
     -r:\'/Applications/Unity/PlaybackEngines/iOSSupport/Variations/il2cpp/Managed/UnityEngine.dll\''
    if marketCode   == "APPLE"  :
        option = option + ' -define:UNITY_IOS'
    elif marketCode == "GOOGLE" :
        option = option + ' -define:UNITY_ANDROID'
    elif marketCode == "MYCARD" :
        option = option + ' -define:UNITY_ANDROID'

    if versionKind   == "DEV_VER"   :
        option = option + ' -define:DEV_VER'
    elif versionKind == "QA_VER"    :
        option = option + ' -define:QA_VER'
    elif versionKind == "IAP_VER"   :
        option = option + ' -define:IAP_VER'
    elif versionKind == "DIST_VER"  :
        option = option + ' -define:DIST_VER'

    return option;


def main() :
    if len(sys.argv) < 4 :
        print("Usage: marketCode versionKind versionHeaderFile")
        return -1
    marketCode          = sys.argv[1]
    versionKind         = sys.argv[2]
    versionHeaderFile   = sys.argv[3]

    print("Get Client Header Version...")



    getClientVersionInHeaderFile(marketCode, versionKind, versionHeaderFile);


if __name__ == "__main__" :
    main()