<template>
  <div>
    <div>
    <b-jumbotron header="TweetSysis"
                 lead="Explore trending hashtags in different cities.
                 See popular tweets. Analyze their sentiment with textBlob. ">
    </b-jumbotron>
    </div>
    <b-container>
      <b-row>
        <b-col>
          <h2>Today's trends</h2>
          <p> Select location to see trending Twitter topics: </p>
          <div>
            <b-button-group>
              <b-button @click="onGetTrends(Seattle)">Seattle</b-button>
              <b-button @click="onGetTrends(Sydney)">Sydney</b-button>
              <b-button @click="onGetTrends(London)">London</b-button>
              <b-button @click="onGetTrends(Toronto)">Toronto</b-button>
            </b-button-group>
            <br>
            <b-table hover :items="trends" :fields="fields" v-if="showTrends">

            </b-table>
          </div>
        </b-col>
        <b-col>2 of 3</b-col>
        <b-col>3 of 3</b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      trends: [],
      showTrends: false,
      fields: [],
    };
  },
  methods: {
    getTrends(location) {
      const path = `http://localhost:5000/trends/${location}`;
      axios.get(path)
        .then(() => {
          this.trends = res.data.trends;
          this.showTrends = true;
          this.fields=['name','tweet_volume']
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    onGetTrends(location) {
      this.getTrends(location);
    },
  },
};
</script>
