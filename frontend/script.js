const API_URL = "https://reconai-8n0t.onrender.com";


/* =========================================
   ELEMENTS
========================================= */

const runButton =
    document.getElementById("runButton");

const buttonText =
    document.getElementById("buttonText");

const buttonIcon =
    document.getElementById("buttonIcon");

const statusMessage =
    document.getElementById("statusMessage");

const totalRecords =
    document.getElementById("totalRecords");

const matchedRecords =
    document.getElementById("matchedRecords");

const manualReview =
    document.getElementById("manualReview");

const unresolvedRecords =
    document.getElementById("unresolvedRecords");

const matchRate =
    document.getElementById("matchRate");

const accuracy =
    document.getElementById("accuracy");

const throughput =
    document.getElementById("throughput");

const matchRateBar =
    document.getElementById("matchRateBar");

const accuracyBar =
    document.getElementById("accuracyBar");

const resultsTableBody =
    document.getElementById("resultsTableBody");

const resultCount =
    document.getElementById("resultCount");

const exceptionCount =
    document.getElementById("exceptionCount");

const exceptionsList =
    document.getElementById("exceptionsList");

const auditTrail =
    document.getElementById("auditTrail");

const searchInput =
    document.getElementById("searchInput");

const decisionFilter =
    document.getElementById("decisionFilter");

const investigationCount =
    document.getElementById("investigationCount");

const investigationList =
    document.getElementById("investigationList");

const totalProcessedAmount =
    document.getElementById("totalProcessedAmount");

const reconciledAmount =
    document.getElementById("reconciledAmount");

const amountUnderReview =
    document.getElementById("amountUnderReview");

const highPriorityCases =
    document.getElementById("highPriorityCases");

const agentRecommendation =
    document.getElementById("agentRecommendation");

const priorityList =
    document.getElementById("priorityList");

const batchStatus =
    document.getElementById("batchStatus");

const executiveRecommendation =
    document.getElementById("executiveRecommendation");

const immediateActions =
    document.getElementById("immediateActions");

const monitoringActions =
    document.getElementById("monitoringActions");

const manualReviewActions =
    document.getElementById("manualReviewActions");

const sidebar =
    document.getElementById("sidebar");

const sidebarToggle =
    document.getElementById("sidebarToggle");

const navItems =
    document.querySelectorAll(".nav-item");


/* =========================================
   APPLICATION STATE
========================================= */

let allResults = [];

let visibleRecords = 10;

let showAllPriorities = false;

let expandedActionContainers = {};


/* =========================================
   SIDEBAR NAVIGATION
========================================= */

sidebarToggle.addEventListener(
    "click",
    () => {

        sidebar.classList.toggle("open");

    }
);


navItems.forEach(item => {

    item.addEventListener(
        "click",
        () => {

            navItems.forEach(nav => {

                nav.classList.remove("active");

            });

            item.classList.add("active");


            if (
                window.innerWidth <= 800
            ) {

                sidebar.classList.remove(
                    "open"
                );

            }

        }
    );

});


/* =========================================
   ACTIVE NAVIGATION ON SCROLL
========================================= */

const sections =
    document.querySelectorAll("main section");


window.addEventListener(
    "scroll",
    () => {

        let currentSection = "";


        sections.forEach(section => {

            const sectionTop =
                section.offsetTop - 150;

            const sectionHeight =
                section.offsetHeight;


            if (
                window.scrollY >= sectionTop
                &&
                window.scrollY <
                sectionTop + sectionHeight
            ) {

                currentSection =
                    section.getAttribute("id");

            }

        });


        if (!currentSection) {

            return;

        }


        navItems.forEach(item => {

            item.classList.remove(
                "active"
            );


            if (
                item.getAttribute("href") ===
                `#${currentSection}`
            ) {

                item.classList.add(
                    "active"
                );

            }

        });

    }
);


/* =========================================
   RUN RECONCILIATION
========================================= */

runButton.addEventListener(
    "click",
    runReconciliation
);


async function runReconciliation() {

    setLoadingState();


    try {

        const response =
            await fetch(
                `${API_URL}/reconcile`
            );


        if (!response.ok) {

            throw new Error(
                "Unable to connect to ReconAI backend."
            );

        }


        const data =
            await response.json();


        allResults =
            data.results;


        visibleRecords = 10;


        updateDashboard(data);


        statusMessage.textContent =
            "Reconciliation completed successfully. " +
            `${data.summary.total_records} records analyzed.`;


        statusMessage.style.color =
            "var(--success)";

    }


    catch (error) {

        console.error(error);


        statusMessage.textContent =
            "Unable to connect to the ReconAI server. " +
            "Make sure FastAPI is running on port 8000.";


        statusMessage.style.color =
            "var(--danger)";

    }


    finally {

        resetButton();

    }

}


/* =========================================
   LOADING STATE
========================================= */

function setLoadingState() {

    runButton.disabled = true;


    buttonText.textContent =
        "Analyzing Records...";


    buttonIcon.textContent =
        "⏳";


    statusMessage.textContent =
        "ReconAI is analyzing financial records...";


    statusMessage.style.color =
        "var(--text-secondary)";

}


function resetButton() {

    runButton.disabled = false;


    buttonText.textContent =
        "Run Reconciliation";


    buttonIcon.textContent =
        "▶";

}


/* =========================================
   UPDATE DASHBOARD
========================================= */

function updateDashboard(data) {

    const summary =
        data.summary;


    updateMetrics(summary);


    updateResultsTable();


    updateExceptions(
        data.exceptions
    );


    updateAuditTrail(
        data.results
    );


    loadInvestigations();


    loadPriorities();


    loadActionPlan();

}


/* =========================================
   AI INVESTIGATION
========================================= */

async function loadInvestigations() {

    try {

        const response =
            await fetch(
                `${API_URL}/investigate`
            );


        if (!response.ok) {

            throw new Error(
                "Unable to load investigations."
            );

        }


        const data =
            await response.json();


        updateInvestigations(
            data.investigations
        );

    }


    catch (error) {

        console.error(
            "Investigation error:",
            error
        );


        investigationList.innerHTML = `

            <div class="empty-exception">

                Unable to load AI investigations.

            </div>

        `;

    }

}


/* =========================================
   PRIORITIES
========================================= */

async function loadPriorities() {

    try {

        const response =
            await fetch(
                `${API_URL}/priorities`
            );


        if (!response.ok) {

            throw new Error(
                "Unable to load priority analysis."
            );

        }


        const data =
            await response.json();


        updateFinancialSummary(
            data.financial_summary
        );


        updatePriorityQueue(
            data.prioritized_exceptions
        );


        updateAgentRecommendation(
            data.financial_summary,
            data.prioritized_exceptions
        );

    }


    catch (error) {

        console.error(
            "Priority analysis error:",
            error
        );


        agentRecommendation.textContent =
            "Unable to generate financial priority analysis.";

    }

}


/* =========================================
   AI ACTION PLAN
========================================= */

async function loadActionPlan() {

    try {

        batchStatus.textContent =
            "ANALYZING";


        const response =
            await fetch(
                `${API_URL}/action-plan`
            );


        if (!response.ok) {

            throw new Error(
                "Unable to load AI action plan."
            );

        }


        const data =
            await response.json();


        updateBatchStatus(
            data.batch_status
        );


        executiveRecommendation.textContent =
            data.executive_recommendation;


        updateActionList(
            immediateActions,
            data.immediate_actions,
            "No immediate actions required."
        );


        updateActionList(
            monitoringActions,
            data.monitoring_actions,
            "No transactions require monitoring."
        );


        updateActionList(
            manualReviewActions,
            data.manual_review_actions,
            "No manual reviews required."
        );

    }


    catch (error) {

        console.error(
            "Action plan error:",
            error
        );


        batchStatus.textContent =
            "UNAVAILABLE";


        executiveRecommendation.textContent =
            "Unable to generate the AI action plan.";

    }

}


/* =========================================
   BATCH STATUS
========================================= */

function updateBatchStatus(status) {

    batchStatus.textContent =
        status.replace(
            "_",
            " "
        );


    batchStatus.className =
        "batch-status";


    if (status === "CRITICAL") {

        batchStatus.classList.add(
            "status-critical"
        );

    }


    else if (
        status === "ATTENTION_REQUIRED"
    ) {

        batchStatus.classList.add(
            "status-attention"
        );

    }


    else if (
        status === "MONITORING"
    ) {

        batchStatus.classList.add(
            "status-monitoring"
        );

    }


    else {

        batchStatus.classList.add(
            "status-healthy"
        );

    }

}


/* =========================================
   ACTION LIST
========================================= */

function updateActionList(
    container,
    actions,
    emptyMessage
) {

    container.innerHTML = "";


    if (
        !actions
        ||
        actions.length === 0
    ) {

        container.innerHTML = `

            <p class="action-empty">

                ${emptyMessage}

            </p>

        `;

        return;

    }


    const containerKey =
        container.id;


    const showAll =
        expandedActionContainers[
            containerKey
        ] || false;


    const visibleActions =
        showAll
            ? actions
            : actions.slice(0, 3);


    visibleActions.forEach(
        action => {

            const item =
                document.createElement(
                    "div"
                );


            item.className =
                "action-item";


            item.innerHTML = `

                <div class="action-transaction">

                    ${action.transaction_id}

                </div>


                <div class="action-description">

                    ${action.recommended_action}

                </div>


                <div class="action-risk">

                    Amount at risk:

                    ${formatCurrency(
                        action.amount_at_risk
                    )}

                </div>

            `;


            container.appendChild(item);

        }
    );


    if (actions.length > 3) {

        const button =
            document.createElement(
                "button"
            );


        button.className =
            "view-all-actions-btn";


        button.textContent =
            showAll
                ? "Show Less"
                : `View All ${actions.length} Cases`;


        button.addEventListener(
            "click",
            () => {

                expandedActionContainers[
                    containerKey
                ] = !showAll;


                updateActionList(
                    container,
                    actions,
                    emptyMessage
                );

            }
        );


        container.appendChild(
            button
        );

    }

}


/* =========================================
   FINANCIAL SUMMARY
========================================= */

function updateFinancialSummary(summary) {

    totalProcessedAmount.textContent =
        formatCurrency(
            summary.total_processed_amount
        );


    reconciledAmount.textContent =
        formatCurrency(
            summary.successfully_reconciled_amount
        );


    amountUnderReview.textContent =
        formatCurrency(
            summary.amount_under_review
        );


    highPriorityCases.textContent =
        summary.high_priority_cases;

}


/* =========================================
   PRIORITY QUEUE
========================================= */

function updatePriorityQueue(priorities) {

    priorityList.innerHTML = "";


    if (
        !priorities
        ||
        priorities.length === 0
    ) {

        priorityList.innerHTML = `

            <div class="empty-exception">

                No financial exceptions require action.

            </div>

        `;

        return;

    }


    const visiblePriorities =
        showAllPriorities
            ? priorities
            : priorities.slice(0, 3);


    visiblePriorities.forEach(
        item => {

            const card =
                document.createElement(
                    "div"
                );


            card.className =
                "priority-card";


            const priorityClass =
                getPriorityClass(
                    item.priority_level
                );


            card.innerHTML = `

                <div class="priority-rank">

                    #${item.rank}

                </div>


                <div class="priority-main">

                    <div class="priority-transaction">

                        ${item.transaction_id}

                    </div>


                    <div class="priority-cause">

                        ${item.probable_cause}

                    </div>


                    <div class="priority-action">

                        💡 ${item.recommended_action}

                    </div>

                </div>


                <div class="priority-right">

                    <div class="priority-amount">

                        ${formatCurrency(
                            item.amount_at_risk
                        )}

                    </div>


                    <span
                        class="
                            priority-badge
                            ${priorityClass}
                        "
                    >

                        ${item.priority_level}

                    </span>

                </div>

            `;


            priorityList.appendChild(
                card
            );

        }
    );


    if (priorities.length > 3) {

        const button =
            document.createElement(
                "button"
            );


        button.className =
            "view-all-priorities-btn";


        button.textContent =
            showAllPriorities
                ? "Show Top 3"
                : `View All ${priorities.length} Priorities`;


        button.addEventListener(
            "click",
            () => {

                showAllPriorities =
                    !showAllPriorities;


                updatePriorityQueue(
                    priorities
                );

            }
        );


        priorityList.appendChild(
            button
        );

    }

}


/* =========================================
   AGENT RECOMMENDATION
========================================= */

function updateAgentRecommendation(
    summary,
    priorities
) {

    if (
        !priorities
        ||
        priorities.length === 0
    ) {

        agentRecommendation.textContent =
            "ReconAI found no financial exceptions requiring immediate action.";

        return;

    }


    const topPriority =
        priorities[0];


    agentRecommendation.textContent =

        `ReconAI detected ${summary.total_exceptions} ` +

        `financial exceptions involving ` +

        `${formatCurrency(summary.amount_under_review)}. ` +

        `The finance team should investigate ` +

        `${topPriority.transaction_id} first because it ` +

        `has a ${topPriority.priority_level.toLowerCase()} ` +

        `priority with ` +

        `${formatCurrency(topPriority.amount_at_risk)} ` +

        `at potential risk.`;

}


/* =========================================
   PRIORITY HELPER
========================================= */

function getPriorityClass(priorityLevel) {

    if (priorityLevel === "CRITICAL") {

        return "priority-critical";

    }


    if (priorityLevel === "HIGH") {

        return "priority-high";

    }


    if (priorityLevel === "MEDIUM") {

        return "priority-medium";

    }


    return "priority-low";

}


/* =========================================
   INVESTIGATIONS
========================================= */

function updateInvestigations(
    investigations
) {

    investigationList.innerHTML = "";


    investigationCount.textContent =
        `${investigations.length} investigated`;


    if (investigations.length === 0) {

        investigationList.innerHTML = `

            <div class="empty-exception">

                No exceptions require investigation.

            </div>

        `;

        return;

    }


    investigations.forEach(
        investigation => {

            const card =
                document.createElement(
                    "div"
                );


            card.className =
                "investigation-card";


            const riskClass =
                getRiskClass(
                    investigation.risk_level
                );


            card.innerHTML = `

                <div class="investigation-top">

                    <div class="investigation-id">

                        ${investigation.transaction_id}

                    </div>


                    <span
                        class="
                            risk-badge
                            ${riskClass}
                        "
                    >

                        ${investigation.risk_level}
                        RISK

                    </span>

                </div>


                <div class="investigation-content">


                    <div class="investigation-item">

                        <p>
                            PROBABLE CAUSE
                        </p>

                        <span>

                            ${investigation.probable_cause}

                        </span>

                    </div>


                    <div class="investigation-item">

                        <p>
                            RECOMMENDED ACTION
                        </p>

                        <span>

                            ${investigation.recommended_action}

                        </span>

                    </div>


                    <div class="investigation-item">

                        <p>
                            CONFIDENCE SCORE
                        </p>

                        <span>

                            ${investigation.confidence_score}%

                        </span>

                    </div>


                </div>

            `;


            investigationList.appendChild(
                card
            );

        }
    );

}


/* =========================================
   RISK HELPER
========================================= */

function getRiskClass(riskLevel) {

    if (riskLevel === "HIGH") {

        return "risk-high";

    }


    if (riskLevel === "MEDIUM") {

        return "risk-medium";

    }


    return "risk-low";

}


/* =========================================
   METRICS
========================================= */

function updateMetrics(summary) {

    animateNumber(
        totalRecords,
        summary.total_records
    );


    animateNumber(
        matchedRecords,
        summary.matched
    );


    animateNumber(
        manualReview,
        summary.manual_review
    );


    animateNumber(
        unresolvedRecords,
        summary.unresolved
    );


    matchRate.textContent =
        `${summary.match_rate}%`;


    accuracy.textContent =
        `${summary.accuracy}%`;


    throughput.textContent =
        summary.throughput_records_per_second;


    setTimeout(
        () => {

            matchRateBar.style.width =
                `${summary.match_rate}%`;


            accuracyBar.style.width =
                `${summary.accuracy}%`;

        },
        100
    );

}


/* =========================================
   NUMBER ANIMATION
========================================= */

function animateNumber(
    element,
    target
) {

    let current = 0;

    const duration = 700;

    const stepTime = 20;

    const steps =
        duration / stepTime;

    const increment =
        target / steps;


    const counter =
        setInterval(
            () => {

                current += increment;


                if (
                    current >= target
                ) {

                    element.textContent =
                        target;


                    clearInterval(counter);

                }

                else {

                    element.textContent =
                        Math.floor(current);

                }

            },
            stepTime
        );

}


/* =========================================
   FILTER RESULTS
========================================= */

function getFilteredResults() {

    const searchText =
        searchInput.value
            .trim()
            .toLowerCase();


    const selectedDecision =
        decisionFilter.value;


    return allResults.filter(
        result => {

            const matchesSearch =
                result.transaction_id
                    .toLowerCase()
                    .includes(searchText);


            const matchesDecision =
                selectedDecision === "ALL"
                ||
                result.decision ===
                selectedDecision;


            return (
                matchesSearch
                &&
                matchesDecision
            );

        }
    );

}


/* =========================================
   RESULTS TABLE
========================================= */

function updateResultsTable() {

    const filteredResults =
        getFilteredResults();


    const recordsToShow =
        filteredResults.slice(
            0,
            visibleRecords
        );


    resultsTableBody.innerHTML = "";


    if (
        recordsToShow.length === 0
    ) {

        resultsTableBody.innerHTML = `

            <tr class="empty-row">

                <td colspan="5">

                    No transactions found.

                </td>

            </tr>

        `;


        resultCount.textContent =
            "0 transactions found";


        return;

    }


    recordsToShow.forEach(
        result => {

            const row =
                document.createElement(
                    "tr"
                );


            const decisionClass =
                getDecisionClass(
                    result.decision
                );


            row.innerHTML = `

                <td>

                    ${result.transaction_id}

                </td>


                <td class="amount">

                    ₹${result.gateway_amount}

                </td>


                <td>

                    ${
                        result.bank_reference
                        || "—"
                    }

                </td>


                <td class="confidence">

                    ${result.confidence_score}%

                </td>


                <td>

                    <span
                        class="
                            decision
                            ${decisionClass}
                        "
                    >

                        ${formatDecision(
                            result.decision
                        )}

                    </span>

                </td>

            `;


            resultsTableBody.appendChild(
                row
            );

        }
    );


    resultCount.textContent =
        `${filteredResults.length} transactions`;


    updateShowMoreButton(
        filteredResults.length
    );

}


/* =========================================
   SHOW MORE
========================================= */

function updateShowMoreButton(
    totalFiltered
) {

    let showMoreButton =
        document.getElementById(
            "showMoreButton"
        );


    if (
        visibleRecords >=
        totalFiltered
    ) {

        if (showMoreButton) {

            showMoreButton.remove();

        }

        return;

    }


    if (!showMoreButton) {

        showMoreButton =
            document.createElement(
                "button"
            );


        showMoreButton.id =
            "showMoreButton";


        showMoreButton.className =
            "show-more-button";


        showMoreButton.textContent =
            "Show More Transactions";


        document
            .querySelector(".table-wrapper")
            .after(showMoreButton);

    }


    showMoreButton.onclick =
        () => {

            visibleRecords += 10;

            updateResultsTable();

        };

}


/* =========================================
   SEARCH AND FILTER
========================================= */

searchInput.addEventListener(
    "input",
    () => {

        visibleRecords = 10;

        updateResultsTable();

    }
);


decisionFilter.addEventListener(
    "change",
    () => {

        visibleRecords = 10;

        updateResultsTable();

    }
);


/* =========================================
   EXCEPTIONS
========================================= */

function updateExceptions(
    exceptions
) {

    exceptionsList.innerHTML = "";


    exceptionCount.textContent =
        `${exceptions.length} requires attention`;


    if (
        exceptions.length === 0
    ) {

        exceptionsList.innerHTML = `

            <div class="empty-exception">

                No exceptions detected.

                All transactions were reconciled.

            </div>

        `;

        return;

    }


    exceptions.forEach(
        exception => {

            const card =
                document.createElement(
                    "div"
                );


            card.className =
                "exception-card";


            const reasons =
                exception.reasons.join(
                    " • "
                );


            card.innerHTML = `

                <div class="exception-top">


                    <div class="exception-id">

                        ${exception.transaction_id}

                    </div>


                    <span
                        class="
                            decision
                            ${getDecisionClass(
                                exception.decision
                            )}
                        "
                    >

                        ${formatDecision(
                            exception.decision
                        )}

                    </span>


                </div>


                <div class="exception-reasons">

                    ${reasons}

                </div>

            `;


            exceptionsList.appendChild(
                card
            );

        }
    );

}


/* =========================================
   AUDIT TRAIL
========================================= */

function updateAuditTrail(results) {

    auditTrail.innerHTML = "";


    const importantResults =
        results.slice(0, 8);


    importantResults.forEach(
        result => {

            const auditItem =
                document.createElement(
                    "div"
                );


            auditItem.className =
                "audit-item";


            const reasons =
                result.reasons.join(
                    " • "
                );


            auditItem.innerHTML = `

                <div class="audit-transaction">

                    ${result.transaction_id}

                </div>


                <div class="audit-reason">

                    <strong>

                        ${formatDecision(
                            result.decision
                        )}

                    </strong>

                    <br>

                    ${reasons}

                </div>

            `;


            auditTrail.appendChild(
                auditItem
            );

        }
    );

}


/* =========================================
   DECISION HELPERS
========================================= */

function getDecisionClass(decision) {

    if (decision === "MATCHED") {

        return "matched";

    }


    if (
        decision === "MANUAL_REVIEW"
    ) {

        return "review";

    }


    return "unresolved";

}


function formatDecision(decision) {

    if (
        decision === "MANUAL_REVIEW"
    ) {

        return "MANUAL REVIEW";

    }


    return decision;

}


/* =========================================
   CURRENCY FORMATTER
========================================= */

function formatCurrency(amount) {

    return new Intl.NumberFormat(
        "en-IN",
        {
            style: "currency",
            currency: "INR",
            maximumFractionDigits: 0
        }
    ).format(amount);

}