##================= Sprint Closeout & Release Tag Checklist =================

Release: _________ Major   _________ Minor  _________ Patch 

Type:   [   ] alpha    [   ] beta    [    ] dev   [    ] public

Date/Time Begin:   ____________________________________________

Released by: _________________________________________

NOTE. You should begin this checklist in the main, clean

1. Final Code  - insert into issue as todo items:
Create sprint issue "sprint-v0.18.1"
Create sprint branch "44-sprint-v0181"
Ensure all feature/bugfix branches are merged to `main`  
Clear Problems [Show Warnings] [Show Errors] in IDE:  
Address runtime or type-checking errors  
Review and resolve compiler warnings:  
Search "Show Infos" `TODO`, `FIXME`, `HACK` comments:  
Convert critical items into GitHub issues  
Add `// TODO (backlog)` to non-sprint TODOs  
Remove stale or irrelevant TODOs 
Label open issues [CARRYFORWARD] and move to later milestone
Update README.md
Update CHANGELOG.md
Run python build script --autobuild
Run verification test case
Verify no runtime exceptions
Verify logs   
Run: `git tag -d v0.18.1`

==============PAGE BREAK===============
<div style="page-break-after: always;"></div>

8. Commit Final Documents/Tags 
git add .
git commit -m "Sprint Release v0.18.1"
git tag -a v0.18.1 -m "Release v0.18.1"
git push origin 44-sprint-v0181
git push origin v0.18.1


10. Create Sprint Artifacts  
   [ ] Copy sprint documents to release
   [ ] Create .ZIP of release
   [ ] Publish .ZIP release in pubmukmuk

11. Close GitHub Milestone  
   [ ] Review milestone issues:  
   [ ] Mark completed  
   [ ] Label uncompleted as `carry-forward`  
   [ ] Close milestone `vX.Y.Z`

12. Start Next Sprint Prep  
   [ ] Create new milestone `vX.Y+1.0`  
   [ ] Optionally create branch `sprint/x-y-z-dev`  
   [ ] Groom backlog and select next sprint stories

13. Notify Team / Stakeholders  
   [ ] Share release summary and tag reference  
   [ ] Confirm milestone closed on GitHub  
   [ ] (Optional) Draft release notes on GitHub using `CHANGELOG.md`

Date/Time Completed:   ____________________________________________

##============================================================================

Author: Mike Mattinson
Updated: Feb/11/2026
