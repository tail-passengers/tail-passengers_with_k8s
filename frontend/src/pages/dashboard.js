import { getCSRFToken } from "../utils/cookie.js";
import { fetchChartData, fetchGameLogs } from "../utils/fetches.js";
import { getCurrentLanguage } from "../utils/languageUtils.js";
import locales from "../utils/locales/locales.js";
import Chart from "chart.js/auto";
import { navigate } from "../utils/navigate.js";
import { $ } from "../utils/querySelector.js";

function Dashboard({ initialState }) {
  this.state = initialState;
  this.$element = document.createElement("div");
  this.$element.className =
    "content tp-ds-content default-container tp-sl-card-content";
  this.$chartCanvas = null;
  this.myChart = null;

  const language = getCurrentLanguage();
  const locale = locales[language] || locales.en;

  this.setState = () => {
    this.render();
  };

  this.render = async () => {
    this.removeLanguageChangeListener = () => {
      // 페이지를 떠날 때 언어 변경 이벤트 리스너를 제거합니다.
      window.removeEventListener("languageChange", this.handleLanguageChange);
    };

    this.$element.innerHTML = `
					<div class="content default-container" style="width:100%;">
							<div class="sized-box"></div>
							<div class="sized-box"></div>
							<div class="home-top-container">
									<canvas id="bar-chart" style="flex:1;"></canvas>
									<div id="records-box">
											<ul id="records-list"></ul>
									</div>
							</div>
							<div class="sized-box"></div>
							<div class="sized-box"></div>
					</div>
			`;

    this.$chartCanvas = document.getElementById("bar-chart");

    const csrfToken = getCSRFToken();
    if (csrfToken !== null) {
      const apiResponse = await fetchChartData();
      const gameLogs = await fetchGameLogs();
      const houseRates = apiResponse.house;
      const userRates = apiResponse.rate;

      this.renderChart(houseRates, userRates);
      this.renderRecords(gameLogs);
    }

    window.addEventListener("beforeunload", this.removeLanguageChangeListener);
  };

  this.renderRecords = (gameLogs) => {
    const limitedGameLogs = gameLogs.slice(0, 5);

    const recordsList = document.getElementById("records-list");
    if (recordsList) {
      recordsList.innerHTML = "";
    } else {
      return;
    }

    limitedGameLogs.forEach((log) => {
      const user1 = log.player1.nickname;
      const user2 = log.player2.nickname;
      const user1Score = log.player1_score;
      const user2Score = log.player2_score;

      const li = document.createElement("li");
      li.textContent = `${user1} [${user1Score}] vs [${user2Score}] ${user2}`;
      li.style.color = "black";
      recordsList.appendChild(li);
    });

    this.renderMoreButton(gameLogs);
  };

  this.renderMoreButton = (gameLogs) => {
    const recordsList = document.getElementById("records-list");

    if (gameLogs.length > 0) {
      const moreButton = document.createElement("button");
      moreButton.classList.add("more-button");
      moreButton.addEventListener("click", () => {
        navigate("/records");
      });
      recordsList.appendChild(moreButton);
      this.updateMoreButtonText(moreButton);
    }
  };

  this.updateMoreButtonText = (moreButton) => {
    const language = getCurrentLanguage();
    const locale = locales[language] || locales.en;
    moreButton.textContent = locale.home.more;
  };

  this.renderChart = (houseRates, userRates, locale) => {
    const labels = Object.keys(houseRates);
    const datasets = [];

    const houseDataset = {
      label: "House",
      data: [],
      backgroundColor: "rgba(255, 99, 132, 0.5)",
      borderColor: "rgba(255, 99, 132, 1)",
      borderWidth: 1,
    };

    const rateDataset = {
      label: "My_rate",
      data: [],
      backgroundColor: "rgba(54, 162, 235, 0.5)",
      borderColor: "rgba(54, 162, 235, 1)",
      borderWidth: 1,
    };

    labels.forEach((label) => {
      houseDataset.data.push((houseRates[label] * 100).toFixed(2));
      rateDataset.data.push((userRates[label] * 100).toFixed(2));
    });

    rateDataset.data.push((userRates.total * 100).toFixed(2));
    datasets.push(houseDataset);
    datasets.push(rateDataset);

    const ctx = this.$chartCanvas.getContext("2d");
    this.myChart = new Chart(
      ctx,
      {
        type: "bar",
        data: {
          labels: labels,
          datasets: datasets,
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: "Winning Rate (%)",
              },
              ticks: {
                stepSize: 20,
              },
            },
          },
          plugins: {
            title: {
              display: true,
              font: {
                size: 18,
              },
            },
            tooltip: {
              callbacks: {
                label: function (context) {
                  const datasetLabel = context.dataset.label || "";
                  const value = context.parsed.y;
                  return `${datasetLabel}: ${value.toFixed(2)}%`;
                },
              },
            },
          },
        },
      },
      500
    );
  };

  this.init = () => {
    let parent = $("#app");
    const child = $(".content");
    if (child) {
      parent.removeChild(child);
      parent.appendChild(this.$element);
    }
    let body = $("body");
    const canvas = $("canvas");
    if (canvas) {
      body.removeChild(canvas);
    }
    this.render();
  };

  this.init();
}

export default Dashboard;
