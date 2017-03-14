import java.io.IOException;
import java.util.*;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;

import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.*;
import org.apache.hadoop.mapreduce.lib.output.*;
import org.apache.hadoop.util.*;

/**
 * Created by leon on 3/12/17.
 * map端以"shop_id + date"作为key,　本质就是一个WordCount
 */


public class ShopPayCount_MapReduce extends Configured implements Tool {

    public static class Map extends Mapper<LongWritable, Text, Text, IntWritable>{
        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException{
            String line = value.toString();
            StringTokenizer tokenizer = new StringTokenizer(line, ",");
            String user_id = tokenizer.nextToken();
            String shop_id = tokenizer.nextToken();
            String date = tokenizer.nextToken().substring(0,10);
            context.write(new Text(shop_id + " "+ date), new IntWritable(1));
        }
    }

    public static class Reduce extends Reducer<Text, IntWritable, Text, IntWritable>{
        public void reduce(Text shopIdAndDate, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException{
            int sum = 0;
            for (IntWritable val : values){
                sum += val.get();
            }
            context.write(shopIdAndDate, new IntWritable(sum));
        }
    }

    public int run(String[] args) throws Exception{
        Job job = new Job(getConf());
        job.setJarByClass(ShopPayCount_MapReduce.class);
        job.setJobName("shop_pay_count");

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        job.setMapperClass(ShopPayCount_MapReduce.Map.class);
        job.setReducerClass(ShopPayCount_MapReduce.Reduce.class);

        job.setInputFormatClass(TextInputFormat.class);
        job.setOutputFormatClass(TextOutputFormat.class);

        FileInputFormat.setInputPaths(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        boolean success = job.waitForCompletion(true);
        return success ? 0:1;
    }
    public static void main(String[] args) throws Exception{
        int ret = ToolRunner.run(new ShopPayCount_MapReduce(), args);
        System.exit(ret);
    }
}
