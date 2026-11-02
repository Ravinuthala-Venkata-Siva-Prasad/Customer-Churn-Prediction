
let churnChart = null;
let subscriptionChart = null;
let contractChart = null;
let ageChart = null;


// Format numbers
function formatNumber(value) {
    return Number(value).toLocaleString("en-IN");
}


// Create or update charts
function createChart(existingChart, canvasId, config) {

    const canvas = document.getElementById(canvasId);

    if (!canvas) return existingChart;

    if (existingChart) {
        existingChart.destroy();
    }

    return new Chart(canvas, config);
}


// Populate dropdowns from actual dataset categories
function populateDropdown(elementId, values) {

    const select = document.getElementById(elementId);

    select.innerHTML = '<option value="">Select an option</option>';

    Object.keys(values || {}).forEach(value => {

        const option = document.createElement("option");

        option.value = value;
        option.textContent = value;

        select.appendChild(option);
    });
}


// Load analytics
async function loadAnalytics() {

    try {

        const response = await fetch("/analytics");

        if (!response.ok) {
            throw new Error("Unable to load analytics.");
        }

        const data = await response.json();


        // KPI cards

        document.getElementById("total-customers").textContent =
            formatNumber(data.total_customers);

        document.getElementById("retained-customers").textContent =
            formatNumber(data.retained_customers);

        document.getElementById("churned-customers").textContent =
            formatNumber(data.churned_customers);

        document.getElementById("churn-rate").textContent =
            data.churn_rate + "%";


        // Populate actual categories from the API

        populateDropdown("subscription", data.subscription_churn);

        populateDropdown("contract", data.contract_churn);


        // Churn doughnut chart

        churnChart = createChart(
            churnChart,
            "churnChart",
            {
                type: "doughnut",

                data: {
                    labels: Object.keys(data.churn_distribution),

                    datasets: [{
                        data: Object.values(data.churn_distribution),
                        backgroundColor: ["#20b981", "#ef5555"],
                        borderWidth: 0,
                        hoverOffset: 8
                    }]
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: false,

                    plugins: {
                        legend: {
                            position: "bottom"
                        }
                    }
                }
            }
        );


        // Subscription chart

        subscriptionChart = createChart(
            subscriptionChart,
            "subscriptionChart",
            {
                type: "bar",

                data: {
                    labels: Object.keys(data.subscription_churn),

                    datasets: [{
                        label: "Churn Rate (%)",
                        data: Object.values(data.subscription_churn),
                        backgroundColor: "#3977f6",
                        borderRadius: 6
                    }]
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: false,

                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    },

                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            }
        );


        // Contract chart

        contractChart = createChart(
            contractChart,
            "contractChart",
            {
                type: "bar",

                data: {
                    labels: Object.keys(data.contract_churn),

                    datasets: [{
                        label: "Churn Rate (%)",
                        data: Object.values(data.contract_churn),
                        backgroundColor: "#8b5cf6",
                        borderRadius: 6
                    }]
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: false,

                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    },

                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            }
        );


        // Age distribution chart

        ageChart = createChart(
            ageChart,
            "ageChart",
            {
                type: "bar",

                data: {
                    labels: Object.keys(data.age_distribution),

                    datasets: [{
                        label: "Number of Customers",
                        data: Object.values(data.age_distribution),
                        backgroundColor: "#f4a62a",
                        borderRadius: 6
                    }]
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: false,

                    plugins: {
                        legend: {
                            display: false
                        }
                    },

                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            }
        );

    } catch (error) {

        console.error("Analytics Error:", error);

        alert("Unable to load dashboard analytics. Check the /analytics API.");
    }
}


// Check model health
async function checkHealth() {

    const statusElement = document.getElementById("model-status");

    try {

        const response = await fetch("/health");

        const data = await response.json();

        if (data.model_loaded) {

            statusElement.textContent = "Model Loaded";

        } else {

            statusElement.textContent = "Model Not Loaded";
        }

    } catch (error) {

        statusElement.textContent = "API Offline";

        console.error(error);
    }
}


// Customer prediction
document.getElementById("prediction-form").addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();

        const button = document.getElementById("predict-button");

        button.disabled = true;
        button.textContent = "Predicting...";


        // Prepare data matching the FastAPI Pydantic model

        const customerData = {

            Age: Number(document.getElementById("age").value),

            Gender: document.getElementById("gender").value.trim(),

            Tenure: Number(document.getElementById("tenure").value),

            Usage_Frequency: Number(
                document.getElementById("usage-frequency").value
            ),

            Support_Calls: Number(
                document.getElementById("support-calls").value
            ),

            Payment_Delay: Number(
                document.getElementById("payment-delay").value
            ),

            Subscription_Type:
                document.getElementById("subscription").value,

            Contract_Length:
                document.getElementById("contract").value,

            Total_Spend: Number(
                document.getElementById("total-spend").value
            ),

            Last_Interaction: Number(
                document.getElementById("last-interaction").value
            )
        };


        try {

            const response = await fetch("/predict", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(customerData)

            });


            const data = await response.json();

            if (!response.ok) {

                throw new Error(
                    data.detail || "Prediction failed."
                );
            }


            // Display prediction

            document.getElementById("prediction-message").textContent =
                data.result;


            const riskElement = document.getElementById("result-risk");

            riskElement.textContent = data.risk + " Risk";

            riskElement.className = "result-risk " +
                (data.risk.toLowerCase() === "high" ? "high" : "low");


            // Probability

            const probability = data.churn_probability;

            const probabilityValue =
                document.getElementById("probability-value");

            const probabilityBar =
                document.getElementById("probability-bar");

            if (probability !== null && probability !== undefined) {

                probabilityValue.textContent = probability + "%";

                probabilityBar.style.width =
                    Math.min(100, Math.max(0, probability)) + "%";

                probabilityBar.style.background =
                    probability >= 50 ? "#ef5555" : "#20b981";

            } else {

                probabilityValue.textContent = "Unavailable";

                probabilityBar.style.width = "0%";
            }


            document.getElementById("result-note").textContent =
                "Prediction generated by your trained machine learning model.";


        } catch (error) {

            console.error("Prediction Error:", error);

            document.getElementById("prediction-message").textContent =
                error.message;

            document.getElementById("result-risk").textContent =
                "Prediction Error";

            document.getElementById("result-risk").className =
                "result-risk";

            document.getElementById("probability-value").textContent =
                "--";

            document.getElementById("probability-bar").style.width =
                "0%";

        } finally {

            button.disabled = false;

            button.textContent = "Predict Customer Churn";
        }

    }
);


// Refresh button
document.getElementById("refresh-btn").addEventListener(
    "click",
    async function() {

        await loadAnalytics();

        await checkHealth();
    }
);


// Start dashboard
document.addEventListener("DOMContentLoaded", function() {

    loadAnalytics();

    checkHealth();

});
