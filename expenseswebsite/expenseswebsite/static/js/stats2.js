// stats2.js
const renderChart2 = (data, labels) => {
    console.log("labels========", labels);
    var ctx2 = document.getElementById("myChart2").getContext("2d");
  
    // Clear the previous chart
    ctx2.clearRect(0, 0, ctx2.canvas.width, ctx2.canvas.height);
  
    // Create and assign the new Chart instance
    window.myChart2 = new Chart(ctx2, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Last 6 months expenses",
            data: data,
            backgroundColor: [
              "rgba(255, 99, 132, 0.2)",
              "rgba(54, 162, 235, 0.2)",
              "rgba(255, 206, 86, 0.2)",
              "rgba(75, 192, 192, 0.2)",
              "rgba(153, 102, 255, 0.2)",
              "rgba(255, 159, 64, 0.2)",
            ],
            borderColor: [
              "rgba(255, 99, 132, 1)",
              "rgba(54, 162, 235, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(153, 102, 255, 1)",
              "rgba(255, 159, 64, 1)",
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        title: {
          display: true,
          text: "Expenses per category",
        },
      },
    });
  };
  
  const getChartData2 = async () => {
    try {
      console.log("fetching");
      const response = await fetch("/expense/expense_category_summary");
      const results = await response.json();
      console.log("results", results);
  
      const category_data = results.expense_category_data;
      const [labels, data] = [
        Object.keys(category_data),
        Object.values(category_data),
      ];
  
      renderChart2(data, labels);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };
  
  window.onload = getChartData2;
  