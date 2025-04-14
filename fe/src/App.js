import { useEffect, useState } from 'react';


function DataPage() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch("http://127.0.0.1:8000/api/data")
            .then(res => {
                if (!res.ok) {
                    throw new Error("Server error: " + res.status);
                }
                return res.json();
            })
            .then(json => {
                setData(json);
                setLoading(false);
            })
            .catch(err => {
                console.error("Chyba při načítání dat:", err);
                setLoading(false);
            });
    }, []);



    if (loading) return <p>Načítání...</p>;
    if (!data) return <p>Žádná data</p>;

    return (
        <div className="p-4">
            <ul className="list-disc pl-4">
                <li><strong>Uživatelské jméno:</strong> {data.author.username}</li>
                <li><strong>Celé jméno:</strong> {data.author.full_name}</li>
                <li><strong>ID:</strong> {data.author.id}</li>
            </ul>
            <ul className="list-disc pl-4">
                <li><strong>caption:</strong>{data.caption}</li>
            </ul>
        </div>
    );
}

export default DataPage;
