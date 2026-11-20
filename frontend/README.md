# Project Title

AI-Powered Agricultural Crop Recommendation System — Frontend Demonstration

- **Developer:** Krithika
- **Role:** Frontend Developer
Local project folder: `Agriculture_Frontend`

## Project Overview

This project is the standalone frontend demonstration for a team-developed AI-powered Agricultural Crop Recommendation System.

The dashboard allows users to adjust seven soil and weather parameters and explore a demonstration of the planned recommendation workflow. It displays three fixed sample crop cards, fictional market information, sample agricultural advisory content, and five simulated agent activity steps.

The current version runs independently in a browser. It does not require the team's repository, a running backend, or an API connection.

The interface demonstrates the frontend user experience only. It does not scientifically calculate crop recommendations or execute AI agents.

## My Role and Responsibilities

Krithika is responsible for frontend development.

Completed responsibilities:

- Created `index.html` for the dashboard structure.
- Created `styles.css` for styling and responsive layouts.
- Created `app.js` for frontend interactions and demonstration rendering.
- Implemented seven sliders with synchronized value displays.
- Built the crop recommendation results dashboard.
- Added demonstration market information.
- Added demonstration agricultural advisory content.
- Built the simulated Agent Trace Viewer.
- Implemented input validation, loading feedback, reset behavior, and frontend error handling.
- Tested the standalone demonstration workflow.

Future frontend responsibilities:

- Integrate with the confirmed backend API contract.
- Display actual backend results and trace information.
- Test frontend and backend interaction.
- Resolve frontend-related integration issues.
- Deploy the frontend when the team reaches the deployment phase.

Backend services, AI agents, orchestration, crop calculations, data preparation, and backend deployment are outside this frontend project's scope.

## Technologies Used

- HTML5
- CSS3
- Vanilla JavaScript
- Browser developer tools for testing

The frontend uses:

- CSS variables for shared design values.
- CSS Grid and Flexbox for layout.
- Responsive media queries.
- Native HTML range inputs.
- JavaScript DOM methods for interaction and rendering.
- `textContent` for inserting display text safely.

No frontend framework, external styling library, npm installation, or build process is required.

## Project Folder Structure

```text
Agriculture_Frontend/
├── index.html
├── styles.css
├── app.js
└── README.md
```

### File purposes

| File | Purpose |
|---|---|
| `index.html` | Dashboard structure, input controls, result containers, status messages, and accessibility markup. |
| `styles.css` | Dashboard appearance, responsive layouts, slider styling, cards, timeline, focus states, and reduced-motion handling. |
| `app.js` | Slider synchronization, validation, simulated processing, demonstration results, reset behavior, and frontend error handling. |
| `README.md` | Setup instructions, implemented features, limitations, testing status, and integration notes. |

Keep `index.html`, `styles.css`, and `app.js` together in the same folder. The HTML references the other two files using relative paths:

- `./styles.css`
- `./app.js`

No image assets are required by the current implementation. Optional asset folders from the initial plan are not runtime dependencies.

## Features Implemented

### Dashboard interface

- Forest-green agricultural dashboard theme.
- Light grey-green background.
- White dashboard panels with rounded corners and subtle shadows.
- Visible demonstration notice.
- Responsive desktop, tablet, and mobile layouts.
- Keyboard focus indicators.
- Reduced-motion preference support.

### Soil and weather inputs

- Seven range sliders.
- Immediate updates to displayed values.
- Units displayed where applicable.
- Validation against the provisional limits and step settings in the HTML.

### Recommendation workflow

- Empty results state on initial page load.
- Recommend Crop button enabled after successful JavaScript initialization.
- Simulated processing delay of approximately 1.2 seconds.
- Loading indicator and status feedback.
- Prevention of duplicate submissions during processing.
- Sliders temporarily disabled during processing.
- Three fixed demonstration crop cards:
  - Rice
  - Maize
  - Chickpea

The display order is fixed. It is not a calculated suitability ranking.

### Market information

- Fictional sample prices for the three demonstration crops.
- Explicit labels stating that prices are not live mandi prices, verified quotes, or forecasts.

### Agricultural advisory

- Sample advisory topics covering soil information, water planning, and local crop planning.
- Clear notices that the content is not personalized farming advice.

### Agent Trace Viewer

Five simulated frontend activity steps:

1. Input validation.
2. Soil agent demonstration.
3. Market agent demonstration.
4. Advisory agent demonstration.
5. Results preparation.

These steps are displayed after the simulated processing delay. They are not streamed backend events or evidence of actual AI agent execution.

### Reset and error handling

- Reset restores original HTML slider defaults.
- Displayed values are synchronized after reset.
- Previous crop, market, advisory, and trace content is cleared.
- Empty states are restored.
- Reset remains available during processing.
- Reset invalidates a pending demonstration so delayed results do not repopulate the dashboard.
- Missing required elements are handled with initialization error messages where possible.
- Validation and rendering errors have dedicated feedback areas.

## Soil and Weather Parameters

The current frontend uses the following provisional demonstration settings:

| Parameter | HTML element ID | Default | Demo range | Step | Display unit |
|---|---|---:|---|---:|---|
| Nitrogen | `nitrogen` | 90 | 0–150 | 1 | Not confirmed |
| Phosphorus | `phosphorus` | 40 | 0–150 | 1 | Not confirmed |
| Potassium | `potassium` | 40 | 0–210 | 1 | Not confirmed |
| Soil pH | `soil-ph` | 6.5 | 0–14 | 0.1 | No unit |
| Temperature | `temperature` | 25 | 0–50 | 0.5 | °C |
| Humidity | `humidity` | 70 | 0–100 | 1 | % |
| Rainfall | `rainfall` | 120 | 0–350 | 1 | mm |

Important:

- These ranges and defaults are demonstration settings, not validated agricultural limits.
- Nitrogen, phosphorus, and potassium units must be confirmed with the team.
- The rainfall measurement period must be confirmed.
- All input units, ranges, steps, and field mappings must be checked against the backend contract before integration.
- HTML input names and IDs do not define the backend request schema.

## How to Run the Project on Windows

### Requirements

- A web browser.
- The three frontend files saved in the same folder.

VS Code is useful for editing but is not required to run the current frontend.

### Run directly from File Explorer

1. Open File Explorer.
2. Locate the `Agriculture_Frontend` folder.
3. Confirm that it contains:
   - `index.html`
   - `styles.css`
   - `app.js`
4. Double-click `index.html`.
5. If prompted, select a web browser.
6. Use the dashboard.

The current version supports direct opening because its demonstration data is stored inside `app.js`. It does not fetch local JSON files, use JavaScript modules, or make backend requests.

### Open and edit in VS Code

1. Open VS Code.
2. Select **File → Open Folder**.
3. Choose `Agriculture_Frontend`.
4. Open the file you want to edit.
5. Save changes using `Ctrl + S`.
6. Return to the browser and refresh.

If the browser still displays an older version, press `Ctrl + F5`.

### Windows filename checks

Ensure that the filenames are exactly:

- `index.html`
- `styles.css`
- `app.js`
- `README.md`

They must not accidentally end with `.txt`.

### Troubleshooting

If the dashboard appears unstyled:

- Confirm that the stylesheet is named `styles.css`.
- Confirm that it is beside `index.html`.
- Refresh with `Ctrl + F5`.

If the buttons remain disabled:

- Confirm that `app.js` exists beside `index.html`.
- Check the browser Console for a script loading or initialization error.
- Confirm that the HTML element IDs match the approved implementation.

If displayed slider values do not update:

- Confirm that JavaScript is enabled.
- Check that `app.js` loaded successfully.
- Review the browser Console.

No `npm install`, development build, or backend startup command is required for this version.

## How to Use the Dashboard

1. Open `index.html`.
2. Read the demonstration notice.
3. Adjust any of the seven sliders.
4. Confirm that the displayed values update.
5. Select **Recommend Crop**.
6. Wait for the short simulated processing delay.
7. Review:
   - Three fixed demonstration crop cards.
   - Fictional sample market prices.
   - Sample advisory topics.
   - Five simulated activity steps.
8. Select **Reset Inputs** to restore the original values and clear the results.

During processing:

- Recommend Crop is temporarily disabled.
- Sliders are temporarily disabled.
- Reset Inputs remains enabled.

Selecting Reset Inputs during processing cancels the pending display operation and restores the empty dashboard.

Changing the sliders does not change the fixed demonstration result set.

## Demonstration Data and Limitations

This project is currently a frontend demonstration, not an operational agricultural recommendation service.

### Current limitations

- No backend is connected.
- No actual API calls are made.
- No `fetch()` calls are used.
- No real AI agents execute.
- No RAG pipeline or agent orchestration runs.
- Crop results are fixed demonstration entries.
- Recommendations are not scientifically calculated from the selected inputs.
- Display order does not indicate calculated crop suitability.
- Market prices are fictional demonstration values.
- Market information is not live mandi data.
- Advisory content is not personalized farming advice.
- Agent Trace entries are simulated frontend events.
- The loading delay is artificial, not a measurement of backend performance.
- Backend integration and deployment are not complete.

### Demonstration-data implementation

The fixed examples are stored in the `demonstrationData` object inside `app.js`.

This object is a frontend display model only. It is not the team's API response schema.

The selected slider values are read and validated, but they are not used to calculate the sample crop results.

Do not use this demonstration to make crop-selection, fertilizer, irrigation, trading, or other farming decisions.

## Backend Integration – Future Work

The frontend will later integrate with Pushpender's FastAPI backend.

Before implementation, confirm the exact API contract with Pushpender and coordinate integration with LK.

Required information includes:

- Local backend base URL.
- Exact endpoint path and method.
- Request field names.
- Required and optional input fields.
- Input data types.
- Units, accepted ranges, and validation rules.
- A complete successful response example.
- Error response structure.
- Crop-result structure and ordering.
- Market and advisory output structures.
- Agent Trace structure and delivery behavior.
- Handling of missing or partially available results.
- Authentication requirements, if any.
- Browser-origin access configuration.

### Planned frontend changes

After the contract is confirmed:

1. Add the actual backend request logic.
2. Map the selected inputs to the confirmed request format.
3. Replace the fixed demonstration data source with actual API responses.
4. Map confirmed backend fields to the dashboard.
5. Update rendering functions where required.
6. Replace simulated trace entries with actual trace information provided by the backend.
7. Add and test network, HTTP, and response-validation error handling.
8. Verify the complete workflow with the team.
9. Update notices so the interface accurately describes the connected mode.

Keep mock behavior explicitly identified if a demonstration mode is retained.

Do not assume that the real response will match `demonstrationData`.

## Expected Integration with FastAPI

The endpoint expected from the project workflow is:

```text
POST /recommend
```

This is a planned integration point, not confirmation that the endpoint is currently running or deployed.

The backend base URL and the exact API contract must be confirmed with Pushpender.

No request JSON or response JSON is specified in this README because those structures have not been confirmed.

The current frontend does not call this endpoint.

### Browser integration considerations

During integration:

- Agree on the frontend's local testing origin.
- Coordinate browser-origin access requirements with Pushpender.
- Confirm whether trace information arrives in the final recommendation response or through another documented mechanism.
- Do not assume that live trace streaming is available.
- Test against the actual backend before claiming integration is complete.

Backend configuration and deployment remain backend-team responsibilities.

## Instructions for the Project Lead (LK)

### Files to integrate

Use the following frontend files together:

- `index.html`
- `styles.css`
- `app.js`
- `README.md`

Place the runtime files together in an agreed frontend directory in the team repository.

For example:

```text
team-repository/
└── frontend/
    ├── index.html
    ├── styles.css
    ├── app.js
    └── README.md
```

This is a suggested integration location, not an assumption about the existing repository structure.

### Integration precautions

- Preserve the relative CSS and JavaScript references unless the directory layout is deliberately changed.
- Preserve existing element IDs unless corresponding JavaScript references are updated.
- Do not treat HTML input names as the agreed API request fields.
- Do not treat `demonstrationData` as a backend response contract.
- Coordinate API details with Pushpender before replacing the mock workflow.
- Confirm input units and ranges with the relevant team members.
- Keep demonstration labels visible while the interface still uses mock data.
- Do not present simulated traces as actual agent execution.
- Do not remove limitations notices before the corresponding functionality is implemented and tested.

### Team ownership

| Team member | Responsibility |
|---|---|
| LK | Project lead, orchestration, and integration coordination. |
| Hruday | Soil and RAG agent. |
| Murali | Market agent. |
| Pushpender | Advisory agent and FastAPI backend. |
| Krithika | Frontend development and frontend integration. |

The standalone frontend does not modify or implement other team members' components.

### Suggested handoff check

Before backend integration:

1. Open the standalone frontend.
2. Confirm that the mock workflow works.
3. Confirm that the limitations are visible.
4. Agree on the frontend location in the team repository.
5. Obtain the confirmed API contract from Pushpender.
6. Plan and test integration as a separate development step.

## Current Development Status

Status: Standalone mock frontend implementation and developer testing complete.

### Tests reported as passed

- All seven sliders update their displayed values.
- Recommend Crop works.
- Three demonstration crop cards are displayed.
- Market information is displayed.
- Agricultural advisory content is displayed.
- Five simulated Agent Trace steps are displayed.
- Reset Inputs restores the original slider values.
- Previous results are cleared after reset.
- No red errors appear in the browser Console.

### Implemented protections for further integration testing

- Duplicate-submission prevention.
- Reset during simulated processing.
- Input validation.
- Missing-element initialization handling.
- Rendering-error feedback.
- Loading-state cleanup.

These protections are implemented in the code. They should remain part of regression testing as the project changes.

### Work not yet completed

- Confirmed backend API contract.
- FastAPI integration.
- Actual agent-result rendering.
- Actual backend trace rendering.
- Frontend/backend end-to-end testing.
- Frontend deployment.
- Public-URL verification with a deployed backend.

The frontend is ready for handoff as a clearly labelled mock demonstration. It is not yet a backend-integrated or deployed application.