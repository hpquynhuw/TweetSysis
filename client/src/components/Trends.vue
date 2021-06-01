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
            <b-form-group>
              <b-form-radio-group
                id="btn-radios-2"
                v-model="selected0"
                button-variant="outline-primary"
                name="radio-btn-outline"
                :options = "options"
                buttons
                @click="onGetTrends(selected0)">
              </b-form-radio-group>
            </b-form-group>
            <br>
            <b-table hover
                     :items="trends" :fields="fields"
                     :select-mode="selectMode"
                      responsive="sm"
                      ref="selectableTable"
                      selectable
                      :tbody-tr-class="rowClass"
                      @row-selected="onRowSelected">
            </b-table>
          </div>
        </b-col>
        <b-col>
          <h3 v-if="showTweets">Tweets Sample on {{selected}}</h3>
          <b-list-group v-for="(tweet, index) in tweets" :key="index">
            <b-list-group-item href="#" class="flex-column align-items-start"
                               v-bind:class="{ 'active' : isSelected(tweet) }"
                               v-on:click="selected2 = tweet">
              <div class="d-flex w-100">
                <small style="padding-left: 240px">
                  {{ tweet.created_at | subStr }} </small>
              </div>
              <p class="mb-1"> {{ tweet.text }} </p>
            </b-list-group-item>
          </b-list-group>
        </b-col>
        <b-col>
          <h2>Sentiment Analysis</h2>
          <p> {{selected2.text}} </p>
          <p> {{sentAna.assessment}} </p>
          <p> {{sentAna.polarity}} </p>
          <p> {{ sentAna.subjectivity}} </p>
        </b-col>
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
      showTweets: false,
      fields: [],
      selectMode: 'single',
      selected: '',
      tweets: [],
      selected2: '',
      selected0: '',
      sentAna: '',
      options: [
        { text: 'Seattle', value: 'Seattle' },
        { text: 'Toronto', value: 'Toronto' },
        { text: 'Sydney', value: 'Sydney' },
        { text: 'London', value: 'London' }],
    };
  },
  filters: {
    subStr(string) {
      return string.substring(0, 10);
    },
  },
  watch: {
    selected0(newVal) {
      this.getTrends(newVal);
    },
    selected2(newVal) {
      this.getSent(newVal);
    },
  },
  methods: {
    getTrends(location) {
      const path = `http://localhost:5000/trends/${location}`;
      axios.get(path)
        .then((res) => {
          this.trends = res.data.trends;
          this.fields = ['name', 'tweet_volume'];
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getTweets(query) {
      const path = 'http://localhost:5000/tweets/';
      axios.post(path, query)
        .then((res) => {
          this.tweets = res.data.tweets.data;
          this.showTweets = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    getSent(text) {
      const path = 'http://localhost:5000/sentiment/';
      axios.post(path, text)
        .then((res) => {
          this.sentAna = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    onGetTrends(location) {
      this.getTrends(location);
    },
    rowClass(item) {
      if (this.selected.includes(item)) {
        return 'table-success';
      }
      return '';
    },
    onRowSelected(items) {
      this.selected = items[0].name;
      this.getTweets(items[0]);
    },
    isSelected(i) {
      return i === this.selected2;
    },
  },
};
</script>

<style>
.list-group {
  padding-bottom: 7px;
  border-radius: 0.5rem;
}
</style>
