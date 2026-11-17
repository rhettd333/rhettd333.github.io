# Search-result correction procedure

Purpose: Refresh an obsolete search snippet after a material biography correction.

Repo only. Never publish this file. Keep it outside the deploy workflow allowlist.

1. Confirm the live page at https://rhettd333.github.io/ serves the corrected text before making a request. Record the check date and the deployed correction commit. Stop if the live text is still wrong.

2. Record the stale snippet exactly as shown, along with the search engine, query, result URL, and date. Keep the record in this file or the run log. Do not add material from the BRIEF.md never-publish list. If exact capture would include it, omit that text and note the omission.

3. For Google, use [URL Inspection in Search Console](https://support.google.com/webmasters/answer/9012289/) and select Request indexing to request a recrawl if access is available. Search Console setup is a separate gated item, G11 in BACKLOG.md. This procedure does not assume it is set up. Without access, record that normal recrawl happens without action. For a snippet that no longer matches the live page, use the [Google Remove Outdated Content tool](https://search.google.com/search-console/remove-outdated-content), now called Refresh outdated content. Follow its [refresh instructions](https://support.google.com/websearch/answer/6349986) for the page URL and obsolete snippet text. Record the submission date and status.

4. For Bing, use [Bing Webmaster Tools URL submission](https://www.bing.com/webmasters/help/URL-Submission-62f2860b) if access is available. Use the [content removal request](https://www.bing.com/webmasters/tools/contentremoval) for an outdated cache or snippet, following the [content removal guidance](https://www.bing.com/webmasters/help/content-removal-cb6c294d). Select the outdated cache or snippet option. Record the submission date and status. If access is unavailable, note that and wait for normal recrawl.

5. Do not submit removal for the whole page when only the snippet is stale. Do not repeat submissions daily or duplicate a pending request. Do not change the corrected page to match the stale snippet. Do not add unsupported biography claims. Refer to the title only as Consultant.

6. Recheck the same query and result after seven days, then weekly until resolved. Record each check date, the snippet shown, and any request status. Record the date the snippet refreshed. A refresh has no fixed deadline. If a request is denied, record the reason and review it before taking further action.

7. Close the record in this file or the run log. Note the outcome, correction commit, request dates, and refresh date. If closed without a refresh, state why and record any follow-up date.
