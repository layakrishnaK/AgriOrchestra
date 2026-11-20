(() => {
  "use strict";

  /*
   * Frontend demonstration only.
   * No backend requests, AI execution, or scientific crop scoring.
   */
  const DEMO_DELAY_MS = 1200;

  const sliderSettings = [
    { id: "nitrogen", label: "Nitrogen", unit: "", decimals: 0 },
    { id: "phosphorus", label: "Phosphorus", unit: "", decimals: 0 },
    { id: "potassium", label: "Potassium", unit: "", decimals: 0 },
    { id: "soil-ph", label: "Soil pH", unit: "", decimals: 1 },
    { id: "temperature", label: "Temperature", unit: " °C", decimals: 1 },
    { id: "humidity", label: "Humidity", unit: "%", decimals: 0 },
    { id: "rainfall", label: "Rainfall", unit: " mm", decimals: 0 }
  ];

  /*
   * This is a local display model, NOT the team's API response schema.
   * These fixed examples do not depend on the slider values.
   * Prices are fictional interface-testing values.
   */
  const demonstrationData = {
    crops: [
      {
        name: "Rice",
        description:
          "Sample crop entry used to test the recommendation card layout.",
        price: "₹2,200 per quintal"
      },
      {
        name: "Maize",
        description:
          "Sample crop entry used to verify a second recommendation card.",
        price: "₹2,000 per quintal"
      },
      {
        name: "Chickpea",
        description:
          "Sample crop entry used to verify a third recommendation card.",
        price: "₹5,000 per quintal"
      }
    ],

    advisory: [
      {
        title: "Soil information",
        text:
          "Example advisory topic: review a recent soil test with a qualified " +
          "local agricultural professional before planning nutrient inputs."
      },
      {
        title: "Water planning",
        text:
          "Example advisory topic: discuss local weather, available water, " +
          "and field conditions when preparing an irrigation plan."
      },
      {
        title: "Local crop planning",
        text:
          "Example advisory topic: consider locally verified growing-season " +
          "and market information before making a crop decision."
      }
    ],

    trace: [
      {
        title: "Input validation",
        text:
          "Simulated frontend event: checked that all seven selected values " +
          "meet the provisional HTML slider constraints."
      },
      {
        title: "Soil agent demonstration",
        text:
          "Simulated frontend event: loaded fixed crop examples. " +
          "No soil agent, RAG pipeline, or scientific scoring ran."
      },
      {
        title: "Market agent demonstration",
        text:
          "Simulated frontend event: loaded fictional sample prices. " +
          "No market agent or live mandi data source was contacted."
      },
      {
        title: "Advisory agent demonstration",
        text:
          "Simulated frontend event: loaded demonstration advisory text. " +
          "No advisory agent generated personalized farming advice."
      },
      {
        title: "Results preparation",
        text:
          "Simulated frontend event: prepared the mock dashboard content. " +
          "These entries are not an actual backend execution log."
      }
    ]
  };

  // All application state stays inside this function scope.
  let elements;
  let sliders = [];
  let isProcessing = false;

  /*
   * Each submission has a version number.
   * Reset changes the version so an old delayed submission cannot
   * unexpectedly repopulate the dashboard.
   */
  let workflowVersion = 0;

  function getRequiredElement(id) {
    const element = document.getElementById(id);

    if (!element) {
      throw new Error(`Required page element is missing: #${id}`);
    }

    return element;
  }

  function collectElements() {
    const requiredIds = [
      "recommendation-form",
      "recommend-button",
      "reset-button",
      "setup-notice",
      "validation-error",
      "application-error",
      "loading-state",
      "recommendation-status",
      "recommendation-section",
      "results-empty-state",
      "crop-results",
      "market-empty-state",
      "market-results",
      "advisory-empty-state",
      "advisory-results",
      "trace-empty-state",
      "agent-trace"
    ];

    const found = {};

    requiredIds.forEach((id) => {
      found[id] = getRequiredElement(id);
    });

    sliders = sliderSettings.map((setting) => {
      const input = getRequiredElement(setting.id);
      const output = getRequiredElement(`${setting.id}-value`);

      if (
        !(input instanceof HTMLInputElement) ||
        input.type !== "range"
      ) {
        throw new Error(`#${setting.id} must be a range input.`);
      }

      return { ...setting, input, output };
    });

    return found;
  }

  function updateSliderDisplay(slider) {
    const value = slider.input.valueAsNumber;

    if (!Number.isFinite(value)) {
      slider.output.textContent = "Invalid value";
      return;
    }

    // Keep pH to one decimal; avoid unnecessary ".0" for temperature.
    let formattedValue = String(value);

    if (slider.id === "soil-ph") {
      formattedValue = value.toFixed(slider.decimals);
    } else if (!Number.isInteger(value)) {
      formattedValue = value.toFixed(slider.decimals);
    }

    slider.output.textContent = `${formattedValue}${slider.unit}`;
  }

  function updateAllSliderDisplays() {
    sliders.forEach(updateSliderDisplay);
  }

  function clearErrors() {
    ["validation-error", "application-error"].forEach((id) => {
      elements[id].textContent = "";
      elements[id].hidden = true;
    });

    sliders.forEach(({ input }) => {
      input.removeAttribute("aria-invalid");
    });
  }

  function showError(id, message) {
    elements[id].textContent = message;
    elements[id].hidden = false;
  }

  function clearResultContent() {
    const sections = [
      ["crop-results", "results-empty-state"],
      ["market-results", "market-empty-state"],
      ["advisory-results", "advisory-empty-state"],
      ["agent-trace", "trace-empty-state"]
    ];

    sections.forEach(([resultsId, emptyId]) => {
      elements[resultsId].replaceChildren();
      elements[resultsId].hidden = true;
      elements[emptyId].hidden = false;
    });
  }

  function setProcessing(processing) {
    isProcessing = processing;

    elements["loading-state"].hidden = !processing;
    elements["recommendation-section"].setAttribute(
      "aria-busy",
      String(processing)
    );

    elements["recommend-button"].disabled = processing;
    elements["recommend-button"].textContent = processing
      ? "Preparing Demo…"
      : "Recommend Crop";

    // Freeze the submitted input selection during the short delay.
    sliders.forEach(({ input }) => {
      input.disabled = processing;
    });

    // Reset remains available so the user can cancel the demonstration.
    elements["reset-button"].disabled = false;
  }

  function readAndValidateInputs() {
    const values = {};
    const errors = [];
    let firstInvalidInput = null;

    sliders.forEach(({ id, label, input }) => {
      const value = input.valueAsNumber;
      const min = Number(input.min);
      const max = Number(input.max);

      const invalid =
        !Number.isFinite(value) ||
        value < min ||
        value > max ||
        !input.validity.valid;

      if (invalid) {
        input.setAttribute("aria-invalid", "true");
        errors.push(
          `${label}: choose a valid value between ${min} and ${max}.`
        );

        if (!firstInvalidInput) {
          firstInvalidInput = input;
        }
      } else {
        values[id] = value;
      }
    });

    return { values, errors, firstInvalidInput };
  }

  // Build text safely instead of interpreting strings as HTML.
  function createTextElement(tagName, text, className) {
    const element = document.createElement(tagName);
    element.textContent = text;

    if (className) {
      element.className = className;
    }

    return element;
  }

  function createBadge(text) {
    return createTextElement("span", text, "section-badge");
  }

  function renderCropCards() {
    const fragment = document.createDocumentFragment();

    demonstrationData.crops.forEach((crop, index) => {
      const card = document.createElement("article");

      card.append(
        createBadge(`Demo position ${index + 1}`),
        createTextElement("h3", crop.name),
        createTextElement("p", crop.description),
        createTextElement(
          "small",
          "MOCK DATA · Fixed display order, not a calculated suitability rank."
        )
      );

      fragment.append(card);
    });

    elements["crop-results"].replaceChildren(fragment);
  }

  function renderMarketInformation() {
    const fragment = document.createDocumentFragment();

    demonstrationData.crops.forEach((crop) => {
      const card = document.createElement("article");
      const details = document.createElement("dl");

      details.append(
        createTextElement("dt", "Sample price"),
        createTextElement("dd", crop.price)
      );

      card.append(
        createTextElement("h3", crop.name),
        details,
        createTextElement(
          "small",
          "Fictional demonstration value—not a live mandi price, " +
          "a verified quote, or a price forecast."
        )
      );

      fragment.append(card);
    });

    elements["market-results"].replaceChildren(fragment);
  }

  function renderAdvisory() {
    const fragment = document.createDocumentFragment();

    fragment.append(
      createBadge("DEMONSTRATION · Not personalized farming advice")
    );

    demonstrationData.advisory.forEach((item) => {
      const card = document.createElement("article");

      card.append(
        createTextElement("h3", item.title),
        createTextElement("p", item.text)
      );

      fragment.append(card);
    });

    elements["advisory-results"].replaceChildren(fragment);
  }

  function renderTrace() {
    const fragment = document.createDocumentFragment();

    demonstrationData.trace.forEach((step) => {
      const listItem = document.createElement("li");

      listItem.append(
        createTextElement("h3", step.title),
        createTextElement("p", step.text),
        createTextElement("small", "SIMULATED FRONTEND EVENT")
      );

      fragment.append(listItem);
    });

    elements["agent-trace"].replaceChildren(fragment);
  }

  function renderDemonstrationResults() {
    renderCropCards();
    renderMarketInformation();
    renderAdvisory();
    renderTrace();

    const sections = [
      ["crop-results", "results-empty-state"],
      ["market-results", "market-empty-state"],
      ["advisory-results", "advisory-empty-state"],
      ["agent-trace", "trace-empty-state"]
    ];

    sections.forEach(([resultsId, emptyId]) => {
      elements[resultsId].hidden = false;
      elements[emptyId].hidden = true;
    });
  }

  function wait(milliseconds) {
    return new Promise((resolve) => {
      window.setTimeout(resolve, milliseconds);
    });
  }

  async function handleSubmit(event) {
    event.preventDefault();

    if (isProcessing) {
      return;
    }

    clearErrors();

    const validation = readAndValidateInputs();

    if (validation.errors.length > 0) {
      // Remove stale results so they cannot be mistaken for this attempt.
      clearResultContent();

      showError(
        "validation-error",
        `Please check your inputs. ${validation.errors.join(" ")}`
      );

      elements["recommendation-status"].textContent =
        "The demonstration was not run because an input is invalid.";

      validation.firstInvalidInput?.focus();
      return;
    }

    /*
     * All seven selected values have been read and validated.
     * They are deliberately NOT used to calculate the fixed results.
     */
    const currentVersion = ++workflowVersion;

    clearResultContent();
    elements["results-empty-state"].hidden = true;
    setProcessing(true);

    elements["recommendation-status"].textContent =
      "Preparing fixed mock results. No backend or AI agents are running.";

    try {
      await wait(DEMO_DELAY_MS);

      // Ignore an outdated operation if Reset was used during loading.
      if (currentVersion !== workflowVersion) {
        return;
      }

      renderDemonstrationResults();

      elements["recommendation-status"].textContent =
        "Demonstration complete. Showing three fixed mock crop entries, " +
        "fictional market prices, sample advice, and simulated frontend steps. " +
        "Results were not calculated from the selected inputs.";
    } catch (error) {
      if (currentVersion !== workflowVersion) {
        return;
      }

      console.error("Frontend demonstration failed:", error);
      clearResultContent();

      showError(
        "application-error",
        "The demonstration results could not be displayed. " +
        "Please try again or reset the inputs."
      );

      elements["recommendation-status"].textContent =
        "The demonstration could not be completed.";
    } finally {
      /*
       * Do not let an older operation change the state of a newer one.
       * The active operation always removes its loading state.
       */
      if (currentVersion === workflowVersion) {
        setProcessing(false);
      }
    }
  }

  function restoreInitialState() {
    // Invalidate any delayed submission that is still waiting.
    workflowVersion += 1;

    // defaultValue preserves the original values declared in index.html.
    sliders.forEach(({ input }) => {
      input.value = input.defaultValue;
    });

    updateAllSliderDisplays();
    clearErrors();
    clearResultContent();
    setProcessing(false);

    elements["recommendation-status"].textContent =
      "No demonstration has been run.";
  }

  function handleReset(event) {
    /*
     * Handle reset ourselves so inputs and displayed values are restored
     * together, rather than waiting for the browser's default reset action.
     */
    event.preventDefault();
    restoreInitialState();
  }

  function handleInitializationError(error) {
    console.error("Dashboard initialization failed:", error);

    // Use independent lookups because normal element collection may have failed.
    const recommendButton = document.getElementById("recommend-button");
    const resetButton = document.getElementById("reset-button");
    const notice = document.getElementById("setup-notice");
    const applicationError = document.getElementById("application-error");
    const loadingState = document.getElementById("loading-state");

    if (recommendButton) recommendButton.disabled = true;
    if (resetButton) resetButton.disabled = true;
    if (loadingState) loadingState.hidden = true;

    const message =
      "The dashboard could not initialize because a required page element " +
      "is missing or incorrect. Check that index.html matches the approved " +
      "version, then refresh the page.";

    if (notice) {
      notice.textContent = message;
      notice.hidden = false;
    }

    if (applicationError) {
      applicationError.textContent = message;
      applicationError.hidden = false;
    }
  }

  function initialize() {
    try {
      elements = collectElements();

      /*
       * Use our single validation path so understandable messages
       * appear in the existing validation-error container.
       */
      elements["recommendation-form"].noValidate = true;

      restoreInitialState();

      sliders.forEach((slider) => {
        slider.input.addEventListener("input", () => {
          updateSliderDisplay(slider);

          // Remove outdated validation messages when the user edits a value.
          if (!elements["validation-error"].hidden) {
            clearErrors();
          }
        });
      });

      elements["recommendation-form"].addEventListener(
        "submit",
        handleSubmit
      );

      elements["recommendation-form"].addEventListener(
        "reset",
        handleReset
      );

      elements["setup-notice"].hidden = true;
    } catch (error) {
      handleInitializationError(error);
    }
  }

  // Supports both the existing deferred script and other loading timings.
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize, { once: true });
  } else {
    initialize();
  }
})();