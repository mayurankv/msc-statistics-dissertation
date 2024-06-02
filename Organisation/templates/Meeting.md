<%*
const meeting_id = app.vault.getFiles().filter(file => file.parent.path === "Organisation/Meetings").length;
await tp.file.rename("Supervisor Meeting " + meeting_id)
await tp.file.create_new(tp.file.find_tfile("Organisation/templates/Progress Report"), "Progress Report " + meeting_id, false, app.vault.getAbstractFileByPath("Organisation/Progress Reports"))
_%>
---
time: <% tp.date.now("YYYY-MM-DDTHH:mm:ss") %>
aliases: 
  - "Supervisor Meeting <% tp.date.now("YYYY-MM-DD") %>"
supervisors: "[[Adam Sykulski]]"
attendees:
  - "[[Francesco Ventura]]"
  - "[[Chiara Ottino]]"
  - "[[Weinan He]]"
degree: MSc Statistics Imperial College London
previous progress report: "[[Progress Report <% meeting_id - 1 %>]]"
next progress report: "[[Progress Report <% meeting_id %>]]"
meeting id: <% meeting_id %>
---
# Meeting

## Activity since last meeting

> [!hint] Ideas
>  ![[Progress Report <% meeting_id - 1 %>#Ideas]]
^ideas

> [!hint] Actions Taken
>  ![[Progress Report <% meeting_id - 1 %>#Actions Taken]]
^taken-actions

> [!success] Successfully Completed
>  ![[Progress Report <% meeting_id - 1 %>#Completed]]
^succesful-actions

> [!failure] Problems Encountered
>  ![[Progress Report <% meeting_id - 1 %>#Problems]]
^problems-encountered

> [!danger] Issues identified
>  ![[Progress Report <% meeting_id - 1 %>#Issues]]
^issues-identified

---

## Minutes
%%
Use `ChatM`, or similarly `Chat<Letter>` to add a chat entry for someone whose name starts with `<Letter>`
%%

```chat
{mode=minimal}
# Meeting Minutes started at <% tp.date.now("HH:mm:ss") %>
[Mayuran Visakan=red, Adam Sykulski=blue, Chiara Ottino=yellow, Weinan He=green, Francesco Ventura=pink]


```
^minutes

## Results

> [!todo] Actionable Points
> - [ ] #toComplete
^actionable-points

## Other Notes

#toComplete

---

## Summary

> [!summary]
> #toComplete
^summary
