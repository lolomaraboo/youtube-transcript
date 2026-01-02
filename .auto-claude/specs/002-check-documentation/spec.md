# Quick Spec: Verify Documentation

## Overview
Read-only verification task to ensure README.md documentation accurately reflects the actual codebase, file structure, and installation steps for the YouTube transcript tool project.

## Workflow Type
simple - Single-phase documentation verification with no code modifications

## Task Scope
Verify technical accuracy of README.md against actual project files:
- File existence and permissions (yt_transcript.py, yt-notebooklm-helper.py, requirements.txt)
- Path accuracy in documentation (symlink paths, Obsidian structure)
- CLI options implementation matches documentation
- Documentation completeness (installation, usage, troubleshooting)

**Out of Scope**: Grammar/style review, code execution, documentation modifications

## Success Criteria
- All documented files exist and have correct permissions
- All documented paths are accurate
- All documented CLI options are implemented in the code
- Documentation sections are complete and accurate
- Deliverable: `docs-verification-report.md` with categorized findings (✅ correct, ❌ needs fixing, 💡 improvements)

## Task
Verify that README.md accurately reflects the actual codebase and installation steps.

## Files to Check
- `README.md` - Main documentation file (French)
- `yt_transcript.py` - Main script referenced in docs
- `yt-notebooklm-helper.py` - Helper script referenced in docs
- `requirements.txt` - Dependencies file

## Verification Checklist

### 1. File Existence & Permissions
- [ ] `yt_transcript.py` exists and is executable
- [ ] `yt-notebooklm-helper.py` exists and is executable
- [ ] `requirements.txt` exists and contains `youtube-transcript-api>=0.6.0`

### 2. File Paths Accuracy
- [ ] README line 16: Symlink path matches actual project location
- [ ] README line 102: Helper symlink path is correct
- [ ] README line 63: Obsidian structure path is documented

### 3. Command Line Options
- [ ] Verify documented CLI options exist in `yt_transcript.py`:
  - `--copy`
  - `--save`
  - `--title`
  - `--tags`
  - `--languages`
  - `--obsidian-path`

### 4. Documentation Completeness
- [ ] Installation section is complete
- [ ] Usage examples are clear
- [ ] NotebookLM fallback workflow is documented
- [ ] Troubleshooting section covers common issues

## Expected Output
Create `docs-verification-report.md` with:
- ✅ Items that are correct
- ❌ Items that need fixing
- 💡 Suggestions for improvements

## Verification Method
Manual check against actual files and code. No code execution required for this phase.

## Notes
- Documentation is in French - maintain language consistency
- Focus on technical accuracy, not grammar/style
- This is a read-only verification task
