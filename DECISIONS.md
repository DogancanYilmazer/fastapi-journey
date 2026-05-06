1. **Connection Management** — How does your connection manager track connected clients? What happens if a client disconnects mid-vote? Does your app handle this gracefully, or does it crash?

“It shows ‘WebSocket connection closed’ when the connection is lost.

2. **State Storage** — You are storing vote counts in memory. Why did you choose this over writing votes to a database? What breaks if you restart the server? What would need to change to make this production-ready?

We should save it to a database instead of memory.

To keep the project short/simple, I couldn’t add a database :b


3. **Concurrency** — What would happen if two users voted at exactly the same moment? Did you handle this in your implementation? If not, what is the risk?

I did not add explicit locking or transaction handling. In this implementation, two votes at the same time could both be processed, but in a larger or multi-worker setup there is a risk of a lost update if the vote count is read and written at the same time.

4. **REST vs WebSocket** — You now have two ways to vote: `POST /polls/{id}/vote` and the WebSocket. What is the key difference in behavior between them? When would a client prefer one over the other?

The REST endpoint is a simple HTTP request that works with any client, even without WebSocket support. It is good for single votes or when real-time updates are not required.


 What is the difference between voting via `POST /polls/{id}/vote` and voting via the WebSocket? When would you use one over the other? This will be a discussion point during your oral defense.

HTTP request. It is simple, works on older systems, and is good when real-time updates are not needed.
WebSocket voting keeps a live connection between the client and server. It allows vote results to update instantly without refreshing the page, so it is better for real-time applications