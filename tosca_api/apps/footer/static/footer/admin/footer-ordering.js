(function () {
  "use strict";

  document.addEventListener("formset:added", function (event) {
    if (event.detail?.formsetName !== "documents") {
      return;
    }

    const addedOrder = event.target.querySelector(
      'input[name^="documents-"][name$="-display_order"]',
    );
    if (!addedOrder) {
      return;
    }

    const existingOrders = Array.from(
      document.querySelectorAll(
        'input[name^="documents-"][name$="-display_order"]',
      ),
    )
      .filter(function (input) {
        if (input === addedOrder || input.name.includes("__prefix__")) {
          return false;
        }
        const row = input.closest(".inline-related");
        const deleteInput = row?.querySelector('input[name$="-DELETE"]');
        return !deleteInput?.checked;
      })
      .map(function (input) {
        return Number.parseInt(input.value, 10);
      })
      .filter(Number.isFinite);

    addedOrder.value = String(
      existingOrders.length ? Math.max(...existingOrders) + 1 : 0,
    );
  });
})();
