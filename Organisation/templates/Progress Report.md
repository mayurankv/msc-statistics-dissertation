<%*
const meeting_id = app.vault.getFiles().filter(file => file.parent.path === "Organisation/Meetings").length;
_%>
---
time: <% tp.date.now("YYYY-MM-DDTHH:mm:ss") %>
aliases: 
  - "Progress Report <% tp.date.now("YYYY-MM-DD") %>"
supervisors: "[[Adam Sykulski]]"
degree: MSc Statistics Imperial College London
previous supervisor meeting: "[[Supervisor Meeting <% meeting_id %>]]"
next supervisor meeting: "[[Supervisor Meeting <% meeting_id + 1 %>]]"
meeting id: <% meeting_id %>
tags: SupervisorMeetingReport
---
# Progress Report

Points to address:

![[Supervisor Meeting <% meeting_id %>#^actionable-points]]

Overview of previous meeting:

![[Supervisor Meeting <% meeting_id %>#^summary]]

---
## Ideas

#toComplete

## Actions Taken

#toComplete

## Results

### Completed

#toComplete

### Problems

#toComplete

### Issues

#toComplete

## Further Discussion Points 

#toComplete

---

## Summary

> [!summary]
> #toComplete
^summary
