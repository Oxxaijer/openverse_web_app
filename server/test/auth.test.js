const request = require('supertest');
const app = require('../index');

describe('Auth routes', () => {
  it('should return 400 for invalid registration', async () => {
    const res = await request(app).post('/api/auth/register').send({
      email: '',
      password: ''
    });
    expect(res.statusCode).toBe(400);
  });
});
