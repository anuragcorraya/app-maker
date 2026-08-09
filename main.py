#!/usr/bin/env python3
# MADDOX MODZ - Termux Native Android AI Builder
# AI adapters are ordinary Python scripts stored under MaddoxApps/ais.
# The active adapter receives:
#   MADDOX_PROMPT, MADDOX_PROJECT_DIR, MADDOX_APP_NAME,
#   MADDOX_PACKAGE_NAME, MADDOX_SDK
# and is expected to create/update files in MADDOX_PROJECT_DIR.
#
# IMPORTANT:
# - Never put API keys in this file or commit them to GitHub.
# - AI-generated Android projects should request only permissions they actually use.
# - Termux storage access is separate from Android app permissions.

import os, sys, json, shutil, subprocess, time, re
from pathlib import Path
from datetime import datetime

BASE = Path("/sdcard/MaddoxApps") if Path("/sdcard").exists() else Path.home() / "MaddoxApps"
PROJECTS = BASE / "projects"
AIS = BASE / "ais"
META = BASE / ".maddox"
CONFIG = META / "config.json"

R = "\033[0m"; B = "\033[1m"
C = "\033[96m"; G = "\033[92m"; Y = "\033[93m"; E = "\033[91m"; M = "\033[95m"; D = "\033[90m"; W = "\033[97m"

def clr(): os.system("clear")
def pause(): input(f"\n{D}Enter চাপুন...{R}")
def log(s): print(f"{C}[*]{R} {s}")
def ok(s): print(f"{G}[✓]{R} {s}")
def warn(s): print(f"{Y}[!]{R} {s}")
def err(s): print(f"{E}[✗]{R} {s}")
def act(s): print(f"{M}[+]{R} {s}")

def init():
    for p in (PROJECTS, AIS, META):
        p.mkdir(parents=True, exist_ok=True)
    if not CONFIG.exists():
        save({"active_ai": None, "ais": {}})

def load():
    try:
        return json.loads(CONFIG.read_text(encoding="utf-8"))
    except Exception:
        return {"active_ai": None, "ais": {}}

def save(x):
    CONFIG.write_text(json.dumps(x, indent=2), encoding="utf-8")

def run(cmd, cwd=None, env=None, timeout=None):
    try:
        p = subprocess.run(cmd, cwd=str(cwd) if cwd else None,
                           env=env, text=True, capture_output=True,
                           timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT"
    except Exception as e:
        return 1, "", str(e)

def safe_name(s):
    return re.sub(r"[^A-Za-z0-9_-]+", "_", s).strip("_") or "app"

def header(title):
    clr()
    print(C + "+" + "-"*48 + "+" + R)
    print(C + "| " + B + title.center(46) + R + C + " |" + R)
    print(C + "+" + "-"*48 + "+" + R)
    print()

# ---------------- AI adapter management ----------------

def add_ai():
    header("ADD AI")
    print("[1] Python Script")
    print("[2] Import .py file")
    print("[3] Test AI")
    print("[4] Back")
    ch = input("\nSelect: ").strip()

    if ch == "1":
        name = input("AI Name: ").strip()
        if not name:
            err("AI name required"); pause(); return
        fn = safe_name(name) + ".py"
        path = AIS / fn
        print("\nPython script paste করুন। শেষ হলে এক লাইনে __MADDOX_END__ লিখুন:\n")
        lines = []
        while True:
            line = input()
            if line.strip() == "__MADDOX_END__":
                break
            lines.append(line)
        text = "\n".join(lines)
        if not text.strip():
            err("Empty script"); pause(); return
        path.write_text(text, encoding="utf-8")
        cfg = load()
        cfg["ais"][path.stem] = {"name": name, "script": str(path),
                                 "created": datetime.now().isoformat()}
        save(cfg)
        ok(f"AI saved: {path}")
        if input("এখন active করবেন? [y/N]: ").lower() == "y":
            set_active(path.stem)
        pause()

    elif ch == "2":
        src = Path(os.path.expanduser(input("Python .py path: ").strip()))
        if not src.is_file() or src.suffix.lower() != ".py":
            err("Valid .py file দিন"); pause(); return
        name = input(f"AI Name [{src.stem}]: ").strip() or src.stem
        dest = AIS / (safe_name(name) + ".py")
        shutil.copy2(src, dest)
        cfg = load()
        cfg["ais"][dest.stem] = {"name": name, "script": str(dest),
                                 "created": datetime.now().isoformat()}
        save(cfg)
        ok(f"Imported: {dest}")
        if input("এখন active করবেন? [y/N]: ").lower() == "y":
            set_active(dest.stem)
        pause()

    elif ch == "3":
        test_ai()
    elif ch == "4":
        return

def set_active(ai_id):
    cfg = load()
    if ai_id not in cfg["ais"]:
        err("AI not found"); return
    cfg["active_ai"] = ai_id
    save(cfg)
    ok("Active AI: " + cfg["ais"][ai_id]["name"])

def test_ai():
    header("AI STATUS / TEST")
    cfg = load()
    if not cfg["ais"]:
        warn("কোনো AI নেই"); pause(); return
    items = list(cfg["ais"].items())
    for i,(k,a) in enumerate(items,1):
        tag = G+"ACTIVE"+R if k == cfg.get("active_ai") else Y+"READY"+R
        print(f"[{i}] {a['name']} - {tag}")
    x = input("\nTest number (0=back): ").strip()
    if x == "0": return
    try:
        a = items[int(x)-1][1]
    except Exception:
        err("Invalid"); pause(); return
    script = Path(a["script"])
    rc, out, er = run([sys.executable, "-m", "py_compile", str(script)], timeout=30)
    if rc:
        err("Python syntax error")
        print(er)
    else:
        ok("Python syntax OK")
        rc, out, er = run([sys.executable, str(script)], timeout=120)
        print(out)
        if er: print(Y + er + R)
        ok("Test complete" if rc == 0 else f"Exited with code {rc}")
    pause()

# ---------------- Project wizard ----------------

def new_app():
    header("NEW NATIVE ANDROID APP")
    name = input("App Name: ").strip()
    package = input("Package Name [com.maddox.app]: ").strip() or "com.maddox.app"
    logo = input("Logo path [Enter=skip]: ").strip()
    splash = input("Splash path [Enter=skip]: ").strip()

    print("\nSDK: [1] API 30  [2] API 31  [3] API 33  [4] API 34  [5] API 35")
    sdk = {"1":30,"2":31,"3":33,"4":34,"5":35}.get(input("Select [4]: ").strip(), 34)

    print("\nFirebase google-services.json paste করুন। এক লাইনে __JSON_END__ লিখুন;")
    print("অথবা প্রথমেই Enter চাপলে skip.")
    lines=[]
    first=input()
    if first:
        lines=[first]
        while True:
            z=input()
            if z.strip()=="__JSON_END__": break
            lines.append(z)
    firebase="\n".join(lines)

    prompt=input("\nApp idea / AI Prompt: ").strip()
    if not name or not prompt:
        err("App Name এবং AI Prompt required"); pause(); return

    folder=PROJECTS/safe_name(name)
    if folder.exists():
        if input("Project exists. Replace? [y/N]: ").lower() != "y":
            return
        shutil.rmtree(folder)
    folder.mkdir(parents=True)

    meta={"app_name":name,"package_name":package,"sdk":sdk,"prompt":prompt,
          "logo":logo,"splash":splash,"created":datetime.now().isoformat()}
    (folder/"maddox.json").write_text(json.dumps(meta,indent=2),encoding="utf-8")
    if firebase.strip():
        (folder/"google-services.json").write_text(firebase,encoding="utf-8")
    for p in (logo,splash):
        if p and Path(p).is_file():
            shutil.copy2(p,folder/Path(p).name)

    ok(f"Project: {folder}")
    generate(folder, meta)
    pause()

def stream_process(cmd, cwd, env, timeout=900):
    try:
        p=subprocess.Popen(cmd,cwd=str(cwd),env=env,
                           stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                           text=True,bufsize=1)
        start=time.time()
        while True:
            if time.time()-start > timeout:
                p.kill(); return 124
            line=p.stdout.readline()
            if not line:
                if p.poll() is not None: break
                continue
            print(C + "│ " + R + line.rstrip())
        return p.wait()
    except KeyboardInterrupt:
        try: p.kill()
        except Exception: pass
        return 130
    except Exception as e:
        err(str(e)); return 1

def generate(folder, meta):
    cfg=load()
    active=cfg.get("active_ai")
    if not active or active not in cfg["ais"]:
        warn("আগে [2] Add AI থেকে একটি Python AI active করুন.")
        return
    ai=cfg["ais"][active]
    script=Path(ai["script"])
    if not script.exists():
        err("Active AI script missing"); return

    print("\n"+M+"=== AI LIVE EXECUTION ==="+R)
    act("AI: "+ai["name"])
    act("Prompt পাঠানো হচ্ছে...")
    print(D+"AI script-কে project folder দেওয়া হচ্ছে: "+str(folder)+R)

    env=os.environ.copy()
    env.update({
        "MADDOX_APP_NAME":meta["app_name"],
        "MADDOX_PACKAGE_NAME":meta["package_name"],
        "MADDOX_SDK":str(meta["sdk"]),
        "MADDOX_PROMPT":meta["prompt"],
        "MADDOX_PROJECT_DIR":str(folder),
    })

    rc=stream_process([sys.executable,str(script)],folder,env)
    if rc == 0:
        ok("AI generation finished.")
        build(folder)
    else:
        err(f"AI failed with code {rc}")

# ---------------- Build + self-healing loop ----------------

def find_gradle(project):
    if os.name == "nt" and (project/"gradlew.bat").exists():
        return [str(project/"gradlew.bat")]
    if (project/"gradlew").exists():
        try: (project/"gradlew").chmod(0o755)
        except Exception: pass
        return [str(project/"gradlew")]
    if shutil.which("gradle"):
        return ["gradle"]
    return None

def build(project, max_heal=3):
    gradle=find_gradle(project)
    if not gradle:
        warn("Gradle wrapper/gradle পাওয়া যায়নি; build skip.")
        return False

    for attempt in range(1,max_heal+2):
        print("\n"+M+f"=== BUILD ATTEMPT {attempt} ==="+R)
        rc,out,er=run(gradle+["assembleDebug","--stacktrace"],cwd=project,timeout=900)
        text=(out or "")+"\n"+(er or "")
        print(text[-12000:])

        if rc==0:
            ok("Code compiled with zero errors!")
            apks=list(project.rglob("*.apk"))
            if apks:
                ok("APK: "+str(apks[0]))
                if input("Install App এখন খুলবেন? [y/N]: ").lower()=="y":
                    install_apk(apks[0])
            return True

        err("Build error detected.")
        if attempt > max_heal:
            err("Self-healing limit reached.")
            return False

        # Ask the active AI adapter to repair the existing project.
        cfg=load(); active=cfg.get("active_ai")
        if not active or active not in cfg["ais"]:
            return False
        script=Path(cfg["ais"][active]["script"])
        env=os.environ.copy()
        env.update({
            "MADDOX_PROJECT_DIR":str(project),
            "MADDOX_HEAL":"1",
            "MADDOX_BUILD_ERROR":text[-12000:],
            "MADDOX_PROMPT":"Fix the Android build errors in the existing project. "
                            "Inspect the files, make the smallest safe changes, "
                            "and keep the requested app behavior."
        })
        act(f"Self-healing: AI fix pass {attempt}...")
        rc2=stream_process([sys.executable,str(script)],project,env,timeout=900)
        if rc2!=0:
            err("AI repair pass failed.")
            return False
        ok("AI repair pass completed; rebuilding...")

    return False

def install_apk(apk):
    # termux-open delegates to Android's installer UI.
    if shutil.which("termux-open"):
        rc,_,er=run(["termux-open",str(apk)])
        if rc==0: ok("APK installer opened.")
        else: err(er)
    else:
        warn("termux-open পাওয়া যায়নি. APK path: "+str(apk))

# ---------------- Recents / permissions ----------------

def recents():
    header("RECENTS")
    ps=sorted([p for p in PROJECTS.iterdir() if p.is_dir()],
              key=lambda p:p.stat().st_mtime,reverse=True)
    if not ps:
        warn("No projects"); pause(); return
    for i,p in enumerate(ps,1):
        print(f"[{i}] {p.name}")
    x=input("\nSelect (0=back): ").strip()
    if x=="0": return
    try:
        p=ps[int(x)-1]
    except Exception:
        err("Invalid"); pause(); return
    print("\nProject:",p)
    print("Files:")
    for f in list(p.rglob("*"))[:80]:
        if f.is_file(): print("  ",f.relative_to(p))
    pause()

def permission_notes():
    header("ANDROID PERMISSION POLICY")
    print("Maddox AI-কে নির্দেশ দিন: only-required permissions ব্যবহার করতে হবে.\n")
    print("Examples:")
    print("• Camera feature -> CAMERA")
    print("• Notifications on Android 13+ -> POST_NOTIFICATIONS")
    print("• Photos on Android 13+ -> READ_MEDIA_IMAGES / VIDEO as needed")
    print("• Older Android photo access -> READ_EXTERNAL_STORAGE where applicable")
    print("• Modern Android সাধারণ file picker ব্যবহার করলে broad storage permission নাও লাগতে পারে.")
    print("\nMaddox নিজে অপ্রয়োজনীয় সব permission চাইবে না.")
    print("Termux-এর /sdcard access-এর জন্য আলাদা করে:")
    print("  termux-setup-storage")
    pause()

# ---------------- GitHub ----------------

def github(project):
    header("GITHUB PUSH")
    if not shutil.which("git"):
        err("Git নেই. Termux: pkg install git")
        pause(); return
    url=input("GitHub repository URL: ").strip()
    if not url: return
    cmds=[
        ["git","init"],
        ["git","add","."],
        ["git","commit","-m","Maddox generated app"]
    ]
    for c in cmds:
        rc,o,e=run(c,cwd=project)
        if rc and "nothing to commit" not in (e or "").lower():
            err(e); pause(); return
    rc,rem,_=run(["git","remote"],cwd=project)
    if "origin" not in rem.split():
        run(["git","remote","add","origin",url],cwd=project)
    # Push current branch, avoiding assumptions about main/master.
    rc,branch,_=run(["git","branch","--show-current"],cwd=project)
    branch=branch.strip() or "main"
    rc,o,e=run(["git","push","-u","origin",branch],cwd=project,timeout=180)
    if rc==0: ok("Pushed to GitHub.")
    else: err(e)
    pause()

# ---------------- Main menu ----------------

def menu():
    while True:
        clr()
        print(C+"+----------------------------------+"+R)
        print(C+"|                                  |"+R)
        print(C+"|           "+B+"MADDOX MODZ"+R+C+"            |"+R)
        print(C+"|                                  |"+R)
        print(C+"|  [1] new app    [2] add ai       |"+R)
        print(C+"|  [3] recents    [4] ais          |"+R)
        print(C+"|                                  |"+R)
        print(C+"|  Status: "+G+"AI Engine Ready"+R+C+"       |"+R)
        print(C+"|                                  |"+R)
        print(C+"+----------------------------------+"+R)
        print("\n[5] GitHub push  [6] Permission guide  [q] Exit")
        ch=input("\nSelect: ").strip().lower()
        if ch=="1": new_app()
        elif ch=="2": add_ai()
        elif ch=="3": recents()
        elif ch=="4": test_ai()
        elif ch=="5":
            projects=sorted([p for p in PROJECTS.iterdir() if p.is_dir()],
                            key=lambda p:p.stat().st_mtime,reverse=True)
            if not projects: warn("No project"); pause()
            else: github(projects[0])
        elif ch=="6": permission_notes()
        elif ch=="q": break
        else: err("Invalid option"); time.sleep(.8)

if __name__=="__main__":
    try:
        init()
        menu()
    except KeyboardInterrupt:
        print("\n"+Y+"Maddox stopped."+R)
