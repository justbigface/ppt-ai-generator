import express from 'express';
import { randomUUID } from 'crypto';
import fs from 'fs/promises';

const app = express();
app.use(express.json());

app.get('/template/:style?', async (req, res) => {
  const style = req.params.style || 'business';
  try {
    const data = await fs.readFile(`./templates/${style}.json`, 'utf-8');
    res.json(JSON.parse(data));
  } catch {
    res.status(404).json({ error: 'template not found' });
  }
});

app.listen(7000, () => console.log('Template service listening on 7000'));
