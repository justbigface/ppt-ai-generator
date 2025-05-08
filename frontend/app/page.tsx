'use client'
import { useState } from 'react'
import axios from 'axios'

export default function Home() {
  const [title, setTitle] = useState('')
  const [loading, setLoading] = useState(false)
  const [fileUrl, setFileUrl] = useState('')

  const handleGenerate = async () => {
    setLoading(true)
    try {
      const { data } = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/projects`, {
        title
      })
      // naive poll – replace with WS in prod
      const url = `${process.env.NEXT_PUBLIC_API_URL}/files/${data.id}.pptx`
      setTimeout(() => setFileUrl(url), 10000)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="flex flex-col items-center justify-center p-8 gap-4">
      <h1 className="text-3xl font-bold">一键生成 PPT</h1>
      <input
        className="border p-2 w-96 rounded"
        placeholder="输入主题，如：市场营销策略"
        value={title}
        onChange={e => setTitle(e.target.value)}
      />
      <button
        className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
        disabled={!title || loading}
        onClick={handleGenerate}
      >
        {loading ? '生成中…' : '立即生成'}
      </button>
      {fileUrl && (
        <a href={fileUrl} className="underline text-blue-600" download>
          下载生成的 PPT
        </a>
      )}
    </main>
  )
}
